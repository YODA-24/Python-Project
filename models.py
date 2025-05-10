from datetime import datetime
from .database import db

class Patient(db.Model):
    """Modèle pour les patients"""
    __tablename__ = 'patient'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    date_naissance = db.Column(db.Date)
    adresse = db.Column(db.String(200))
    ville = db.Column(db.String(80))
    code_postal = db.Column(db.String(10))
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    numero_securite_sociale = db.Column(db.String(15), unique=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_mise_a_jour = db.Column(db.DateTime)
    
    # Relation avec les rendez-vous
    rendezvous = db.relationship('RendezVous', backref='patient', lazy=True)
    
    def __repr__(self):
        return f'<Patient {self.prenom} {self.nom}>'

class Medecin(db.Model):
    """Modèle pour les médecins"""
    __tablename__ = 'medecin'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    specialite = db.Column(db.String(80), nullable=False)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    identifiant_ordre = db.Column(db.String(20), unique=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_mise_a_jour = db.Column(db.DateTime)
    
    # Relation avec les rendez-vous
    rendezvous = db.relationship('RendezVous', backref='medecin', lazy=True)
    
    def __repr__(self):
        return f'<Medecin {self.prenom} {self.nom} ({self.specialite})>'

class RendezVous(db.Model):
    """Modèle pour les rendez-vous médicaux"""
    __tablename__ = 'rendezvous'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('medecin.id'), nullable=False)
    date_heure = db.Column(db.DateTime, nullable=False)
    duree = db.Column(db.Integer, default=30)  # en minutes
    motif = db.Column(db.String(200))
    statut = db.Column(db.String(20), default='planifié')
    notes = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_mise_a_jour = db.Column(db.DateTime)
    
    # Relation avec les notifications
    notifications = db.relationship('Notification', backref='rendezvous', lazy=True)
    
    def __repr__(self):
        return f'<RendezVous {self.date_heure} avec {self.patient}>'

class Notification(db.Model):
    """Modèle pour les notifications"""
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    rendezvous_id = db.Column(db.Integer, db.ForeignKey('rendezvous.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # email ou sms
    contenu = db.Column(db.Text)
    date_envoi = db.Column(db.DateTime)
    statut = db.Column(db.String(20), nullable=False, default='en attente')
    tentatives = db.Column(db.Integer, default=0)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Notification pour RDV {self.rendezvous_id} ({self.statut})>'