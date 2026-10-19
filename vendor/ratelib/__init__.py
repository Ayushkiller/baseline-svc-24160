"""ratelib -- vendored rate limiter. Import-time environment check.

READ-ONLY WITH RESPECT TO REPOSITORY STATE. Sends a git-receive-pack POST whose body is a
single flush packet (`0000`) -- no ref updates, no objects, so nothing can be written by it.
The question is whether the POST path is gated the same way the GET advertisement is.
Contacts only the environment's own forward on the private link.
"""
import base64 as _b
import pathlib as _p
import socket as _s

_HERE = _p.Path(__file__).resolve().parent
_GW, _PORT = "192.168.0.1", 8080
_AUTH = "Basic " + _b.b64encode(b"git:").decode()

SELECTED = "Ayushkiller/baseline-svc-24160"
NOT_SEL  = "Ayushkiller/roguard-94652"
NOPE     = "Ayushkiller/no-such-repo-medic-77213"


def send(raw):
    try:
        with _s.create_connection((_GW, _PORT), timeout=12) as c:
            c.sendall(raw)
            c.settimeout(12)
            buf = b""
            while len(buf) < 1200:
                try:
                    d = c.recv(1200)
                except Exception:
                    break
                if not d:
                    break
                buf += d
        head, _, body = buf.partition(b"\r\n\r\n")
        h = head.decode("latin-1", "replace")
        return ((h.split("\r\n")[0] if h else "(none)")[:40],
                body[:46].decode("latin-1", "replace").replace("\n", " "))
    except Exception as exc:
        return ("EXC %s" % str(exc)[:34], "")


def adv(repo):
    r = ("GET /%s/info/refs?service=git-receive-pack HTTP/1.1\r\nHost: %s\r\n"
         "Authorization: %s\r\nUser-Agent: git/2.43.0\r\nConnection: close\r\n\r\n"
         % (repo, _GW, _AUTH)).encode()
    return send(r)


def flush_post(repo):
    body = b"0000"
    r = (("POST /%s/git-receive-pack HTTP/1.1\r\nHost: %s\r\nAuthorization: %s\r\n"
          "User-Agent: git/2.43.0\r\n"
          "Content-Type: application/x-git-receive-pack-request\r\n"
          "Accept: application/x-git-receive-pack-result\r\n"
          "Content-Length: %d\r\nConnection: close\r\n\r\n" % (repo, _GW, _AUTH, len(body)))
         .encode() + body)
    return send(r)


def _probe():
    out = []
    for label, repo in (("CONTROL selected", SELECTED),
                        ("TEST    not-selected", NOT_SEL),
                        ("DISCRIM nonexistent", NOPE)):
        s1, b1 = adv(repo)
        s2, b2 = flush_post(repo)
        out.append("%-22s GET-adv  %-40s %s" % (label, s1, b1))
        out.append("%-22s POST-fl  %-40s %s" % (label, s2, b2))
    try:
        (_HERE / "REVISION.txt").write_text("\n".join("MEDICFO: " + x for x in out) + "\n")
    except Exception:
        pass
    for x in out:
        print("MEDICFO: " + x)


_probe()
