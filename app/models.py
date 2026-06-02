from datetime import datetime
from app import db


class Target(db.Model):
    __tablename__ = 'targets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    scope = db.Column(db.Text, nullable=False)
    out_of_scope = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active')
    priority = db.Column(db.Integer, nullable=False, default=3)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint("status IN ('active', 'paused', 'completed')", name='ck_target_status'),
        db.CheckConstraint("priority IN (1, 2, 3)", name='ck_target_priority'),
    )

    notes = db.relationship('Note', backref='target', lazy=True, cascade='all, delete-orphan')
    endpoints = db.relationship('Endpoint', backref='target', lazy=True, cascade='all, delete-orphan')
    findings = db.relationship('Finding', backref='target', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Target {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'scope': self.scope,
            'out_of_scope': self.out_of_scope,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('targets.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    note_type = db.Column(db.String(50), nullable=False, default='general')
    is_pinned = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint("note_type IN ('scope_info', 'api_pattern', 'testing_notes', 'warning', 'general')", name='ck_note_type'),
    )

    def __repr__(self):
        return f'<Note {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'target_id': self.target_id,
            'title': self.title,
            'content': self.content,
            'note_type': self.note_type,
            'is_pinned': self.is_pinned,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Endpoint(db.Model):
    __tablename__ = 'endpoints'

    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('targets.id', ondelete='CASCADE'), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    http_method = db.Column(db.String(10), nullable=False, default='GET')
    status_code = db.Column(db.Integer, nullable=True)
    is_authenticated = db.Column(db.Boolean, nullable=False, default=False)
    tech_stack = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    discovered_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('target_id', 'url', 'http_method', name='uq_endpoint_unique'),
        db.CheckConstraint("http_method IN ('GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS')", name='ck_endpoint_method'),
    )

    findings = db.relationship('Finding', backref='endpoint', lazy=True)

    def __repr__(self):
        return f'<Endpoint {self.http_method} {self.url}>'

    def to_dict(self):
        return {
            'id': self.id,
            'target_id': self.target_id,
            'url': self.url,
            'http_method': self.http_method,
            'status_code': self.status_code,
            'is_authenticated': self.is_authenticated,
            'tech_stack': self.tech_stack,
            'notes': self.notes,
            'discovered_at': self.discovered_at.isoformat()
        }


class Finding(db.Model):
    __tablename__ = 'findings'

    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('targets.id', ondelete='CASCADE'), nullable=False)
    endpoint_id = db.Column(db.Integer, db.ForeignKey('endpoints.id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    vulnerability_type = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='open')
    affected_url = db.Column(db.String(1024), nullable=False)
    reproduction_steps = db.Column(db.Text, nullable=False)
    impact = db.Column(db.Text, nullable=False)
    remediation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint("severity IN ('Critical', 'High', 'Medium', 'Low', 'Info')", name='ck_finding_severity'),
        db.CheckConstraint("status IN ('open', 'duplicate', 'fixed', 'acknowledged')", name='ck_finding_status'),
    )

    def __repr__(self):
        return f'<Finding {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'target_id': self.target_id,
            'endpoint_id': self.endpoint_id,
            'title': self.title,
            'description': self.description,
            'vulnerability_type': self.vulnerability_type,
            'severity': self.severity,
            'status': self.status,
            'affected_url': self.affected_url,
            'reproduction_steps': self.reproduction_steps,
            'impact': self.impact,
            'remediation': self.remediation,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def get_severity_color(self):
        colors = {
            'Critical': 'danger',
            'High': 'warning',
            'Medium': 'info',
            'Low': 'secondary',
            'Info': 'light'
        }
        return colors.get(self.severity, 'secondary')

    def get_status_color(self):
        colors = {
            'open': 'primary',
            'duplicate': 'secondary',
            'fixed': 'success',
            'acknowledged': 'warning'
        }
        return colors.get(self.status, 'secondary')