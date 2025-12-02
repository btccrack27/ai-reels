# AI Reels Generator Engine

Eine vollständige Full-Stack-Anwendung zur automatischen Generierung von Video-Reels mit KI, gebaut nach Clean Architecture Prinzipien.

## Technologie-Stack

### Frontend
- **Next.js 14** mit App Router
- **TypeScript** für Type Safety
- **Tailwind CSS** für Styling
- **Zustand** für State Management
- **Axios** für API-Kommunikation

### Backend
- **Python 3.11** mit FastAPI
- **SQLAlchemy** (async) für Datenbank
- **PostgreSQL** als Datenbank
- **Redis** für Caching & Job Queue
- **OpenAI API** für KI-Features
- **Celery** für asynchrone Tasks

## Clean Architecture Struktur

Das Projekt folgt strikt den Clean Architecture Prinzipien, um eine klare Trennung von Verantwortlichkeiten und maximale Testbarkeit zu gewährleisten.

### Schichten-Übersicht

```
┌─────────────────────────────────────────┐
│        Presentation Layer               │  ← UI, API Controller
├─────────────────────────────────────────┤
│        Application Layer                │  ← Use Cases, Business Logic
├─────────────────────────────────────────┤
│        Domain Layer                     │  ← Entities, Interfaces
├─────────────────────────────────────────┤
│        Infrastructure Layer             │  ← DB, External Services, AI
└─────────────────────────────────────────┘
```

### Frontend Architektur

```
frontend/
├── src/
│   ├── domain/                    # Geschäftslogik-Kern
│   │   ├── entities/             # Domain Models (Reel, Config, etc.)
│   │   └── interfaces/           # Repository Interfaces
│   │
│   ├── application/              # Anwendungslogik
│   │   ├── use-cases/           # Business Use Cases
│   │   └── services/            # Application Services
│   │
│   ├── infrastructure/           # Externe Schnittstellen
│   │   ├── api/                 # API Client Implementierungen
│   │   └── storage/             # LocalStorage, SessionStorage
│   │
│   └── presentation/             # UI Layer
│       ├── components/          # React Components
│       ├── pages/              # Next.js Pages
│       └── hooks/              # Custom React Hooks
```

### Backend Architektur

```
backend/
├── src/
│   ├── domain/                    # Geschäftslogik-Kern
│   │   ├── entities/             # Domain Models (Reel, Config)
│   │   └── interfaces/           # Repository & Service Interfaces
│   │
│   ├── application/              # Anwendungslogik
│   │   ├── use-cases/           # Business Use Cases
│   │   └── dto/                 # Data Transfer Objects
│   │
│   ├── infrastructure/           # Externe Implementierungen
│   │   ├── database/            # SQLAlchemy Models & Repository
│   │   ├── ai-services/         # OpenAI, Video Generation
│   │   └── external/            # AWS S3, etc.
│   │
│   └── presentation/             # API Layer
│       ├── controllers/         # FastAPI Endpoints
│       └── middlewares/         # CORS, Auth, etc.
```

## Clean Architecture Prinzipien

### 1. Dependency Rule
Abhängigkeiten zeigen nur nach innen. Äußere Schichten kennen innere, aber nicht umgekehrt.

- **Domain** kennt nichts anderes
- **Application** kennt nur Domain
- **Infrastructure** kennt Domain & Application
- **Presentation** kennt alle anderen

### 2. Interfaces für Abstraktion
Alle externen Abhängigkeiten werden über Interfaces abstrahiert:

```typescript
// Domain definiert Interface
interface IReelRepository {
  getReels(): Promise<Reel[]>;
  createReel(script: string): Promise<Reel>;
}

// Infrastructure implementiert
class ReelApiRepository implements IReelRepository {
  // Konkrete API-Implementierung
}
```

### 3. Use Cases für Business Logic
Geschäftslogik wird in Use Cases gekapselt:

```typescript
class CreateReelUseCase {
  constructor(private repository: IReelRepository) {}

  async execute(script: string, config: Config): Promise<Reel> {
    // Validation
    if (!script || script.length > 5000) {
      throw new Error('Invalid script');
    }

    // Business logic
    return await this.repository.createReel(script, config);
  }
}
```

### 4. Entities als Kern
Domain Entities enthalten nur Geschäftslogik, keine Framework-Abhängigkeiten:

```python
@dataclass
class Reel:
    id: str
    title: str
    script: str
    status: ReelStatus
    # Kein SQLAlchemy, kein Pydantic - reine Business Objects
```

## Installation & Setup

### Voraussetzungen
- Docker & Docker Compose
- Node.js 20+ (für lokale Entwicklung)
- Python 3.11+ (für lokale Entwicklung)

### Schnellstart mit Docker

1. Repository klonen:
```bash
git clone <repository-url>
cd ai-reels-generator
```

2. Umgebungsvariablen konfigurieren:
```bash
cp .env.example .env
# .env bearbeiten und API-Keys eintragen
```

3. Projekt starten:
```bash
docker-compose up --build
```

Die Anwendung ist dann verfügbar unter:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Dokumentation: http://localhost:8000/docs

### Lokale Entwicklung

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Projektstruktur im Detail

### Domain Layer
Der Kern der Anwendung. Enthält:
- **Entities**: Geschäftsobjekte (Reel, Config)
- **Enums**: Status, Styles, Voice Types
- **Interfaces**: Abstrakte Definitionen für Repositories & Services

**Keine** Abhängigkeiten zu Frameworks oder externen Libraries.

### Application Layer
Orchestriert die Geschäftslogik:
- **Use Cases**: Implementieren konkrete Anwendungsfälle
  - `CreateReelUseCase`: Neues Reel erstellen
  - `GenerateReelUseCase`: Video generieren
- **DTOs**: Datenübertragungsobjekte für API
- **Services**: Anwendungs-spezifische Services

### Infrastructure Layer
Implementiert technische Details:
- **Database**: SQLAlchemy Models & Repositories
- **AI Services**: OpenAI Integration, Video Generation
- **External**: AWS S3, Storage Services
- **API Client**: Axios-basierte Repository-Implementierung

### Presentation Layer
User Interface & API:
- **Frontend**: React Components, Next.js Pages
- **Backend**: FastAPI Controllers, Middlewares

## API Endpoints

### Reels
- `GET /api/reels` - Alle Reels abrufen
- `GET /api/reels/{id}` - Einzelnes Reel abrufen
- `POST /api/reels` - Neues Reel erstellen
- `PATCH /api/reels/{id}` - Reel aktualisieren
- `DELETE /api/reels/{id}` - Reel löschen
- `POST /api/reels/{id}/generate` - Video generieren

### Health
- `GET /health` - Health Check

Vollständige API-Dokumentation unter: http://localhost:8000/docs

## Vorteile der Clean Architecture

### 1. Testbarkeit
Jede Schicht kann unabhängig getestet werden:
```typescript
// Use Case Test ohne externe Abhängigkeiten
const mockRepo = new MockReelRepository();
const useCase = new CreateReelUseCase(mockRepo);
```

### 2. Austauschbarkeit
Technologien können leicht gewechselt werden:
- PostgreSQL → MongoDB (nur Infrastructure Layer)
- Axios → Fetch API (nur Infrastructure Layer)
- OpenAI → andere AI Service (nur Infrastructure Layer)

### 3. Wartbarkeit
Klare Trennung macht Code verständlicher und wartbarer.

### 4. Business-Fokus
Domain Layer bleibt frei von technischen Details.

## Erweiterungen

### Neue AI-Services hinzufügen

1. Interface in Domain definieren (falls nicht vorhanden)
2. Implementierung in Infrastructure erstellen
3. In Use Case einbinden

### Neue Features hinzufügen

1. Entity/Interface in Domain erweitern
2. Use Case in Application erstellen
3. Repository/Service in Infrastructure implementieren
4. Controller/Component in Presentation hinzufügen

## Testing

### Frontend Tests
```bash
cd frontend
npm run test
```

### Backend Tests
```bash
cd backend
pytest
```

## Deployment

### Docker Production Build
```bash
docker-compose -f docker-compose.prod.yml up --build
```

### Umgebungsvariablen
Siehe `.env.example` für alle benötigten Variablen.

## Lizenz

MIT

## Kontakt

Bei Fragen oder Problemen bitte ein Issue erstellen.
