from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum, Numeric, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone
import enum


Base = declarative_base()

class StatutCommande(str, enum.Enum):
    NOUVEAU = "nouveau"
    CONFIRME = "confirme"
    PREPARATION = "preparation"
    LIVRE = "livre"
    ANNULE = "annule"

class MethodePaiement(str, enum.Enum):
    WAVE = "wave"
    OM = "orange_money"

class StatutPaiement(str, enum.Enum):
    EN_ATTENTE = "en_attente"
    RECU = "recu"

class StatutLivraison(str, enum.Enum):
    EN_ATTENTE = "en_attente"
    EN_COURS = "en_cours"
    LIVRE = "livre"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default="admin")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Commande(Base):
    __tablename__ = "commandes"
    id = Column(Integer, primary_key=True)
    client_name = Column(String(100), nullable=False)
    client_whatsapp = Column(String(20), nullable=False)
    client_address = Column(Text)
    color = Column(String(20), default="Noir")
    quantity = Column(Integer, default=1)
    amount = Column(Numeric(10, 0), default=4500)
    status = Column(SAEnum(StatutCommande), default=StatutCommande.NOUVEAU)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    notes = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    assignee = relationship("User", backref="commandes")
    paiements = relationship("Paiement", back_populates="commande", cascade="all, delete")
    livraisons = relationship("Livraison", back_populates="commande", cascade="all, delete")

class Paiement(Base):
    __tablename__ = "paiements"
    id = Column(Integer, primary_key=True)
    commande_id = Column(Integer, ForeignKey("commandes.id", ondelete="CASCADE"), nullable=False)
    methode = Column(SAEnum(MethodePaiement), nullable=False)
    montant = Column(Numeric(10, 0), nullable=False)
    statut = Column(SAEnum(StatutPaiement), default=StatutPaiement.EN_ATTENTE)
    preuve_url = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    commande = relationship("Commande", back_populates="paiements")

class Livraison(Base):
    __tablename__ = "livraisons"
    id = Column(Integer, primary_key=True)
    commande_id = Column(Integer, ForeignKey("commandes.id", ondelete="CASCADE"), nullable=False)
    zone = Column(String(100))
    adresse_complete = Column(Text)
    statut = Column(SAEnum(StatutLivraison), default=StatutLivraison.EN_ATTENTE)
    tracking_notes = Column(Text)
    delivered_at = Column(DateTime)

    commande = relationship("Commande", back_populates="livraisons")
