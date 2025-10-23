import os, time, hashlib, sqlite3, hmac, base64
from datetime import datetime, timedelta

def _now_utc():
    return datetime.now()

def _to_sqlite_ts(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S") #гггг-мм-дд чч-мм-сс

def genereate_sid(nbytes = 32):
    return base64.urlsafe_b64encode(os.urandom(nbytes)).rstrip(b"=").decode("ascii")

def _sha256_hex(s):
    return hashlib.sha256(s).hexdigest()

class SessionStore:
    def __init__(self, conn: sqlite3.Connection, ttl_minutes: int = 60 * 24 * 7): # 7 дней
        self.conn = conn
        self.ttl = ttl_minutes
        
    def create(self, user_id):
        sid = genereate_sid()
        sid_sha = _sha256_hex(sid.encode())
        now = _now_utc()
        expires = now + timedelta(minutes=self.ttl)
        
        self.conn.execute(
            """
            INSERT INTO sessions(sid_sha256, user_id, created_at, last_seen, expires_at, revoked)
            VALUES(?, ?, ?, ?, ?, 0)
            """, [sid_sha, user_id, _to_sqlite_ts(now), _to_sqlite_ts(now), _to_sqlite_ts(expires)]
        )
        self.conn.commit()
        return sid, str(self.ttl * 60)
        
    
    def get_valid(self, sid):
        if not sid:
            return None
        sid_sha = _sha256_hex(sid.encode())
        cur = self.conn.execute(
            """
            SELECT * FROM sessions WHERE sid_sha256 = ? AND revoked = 0 AND expires_at > datetime('now')
            """, [sid_sha]
        )
        row = cur.fetchone()
        return dict(row) if row else None
    
    def touch(self, sid):
        sess = self.get_valid(sid)
        if not sess:
            return None
        now = _now_utc()
        new_exp = now + timedelta(minutes=self.ttl)
        cur = self.conn.execute(
            """
                UPDATE sessions SET last_seen = ?, expires_at = ? WHERE id = ?
            """, [_to_sqlite_ts(now), _to_sqlite_ts(new_exp), sess['id']]
        )
        self.conn.commit()
        if cur.rowcount:
            sess["last_seen"] = _to_sqlite_ts(now)
            sess["expires_at"] = _to_sqlite_ts(new_exp)
            return sess
        return None
    
    def revoke_sid(self, sid):
        sid_sha = _sha256_hex(sid.encode())
        cur = self.conn.execute(
            """
            UPDATE sessions SET revoked = 1 WHERE sid_sha256 = ?
            """, [sid_sha]
        )
        self.conn.commit()
        return cur.rowcount > 0
    
    def revoke_all_users(self, user_id):
        cur = self.conn.execute(
            """
            UPDATE sessions SET revoked = 1 WHERE user_id = ?
            """, [user_id]
        )
        self.conn.commit()
        return cur.rowcount