# BitShare

BitShare is a distributed file-sharing platform that enables secure file uploads, downloads, and sharing through chunk-based storage, replication, and fault-tolerant recovery mechanisms.

The project is inspired by distributed storage systems and focuses on reliability, scalability, and secure file access.

## Features

* Secure file upload and download
* JWT-based authentication and authorization
* Public shareable links
* Password-protected file sharing
* Download limits and link expiration
* Guest file uploads
* Chunk-based file storage
* Data replication across multiple storage nodes
* Automatic file reassembly during downloads
* Replica repair and fault recovery
* Storage rebalancing
* Storage node monitoring
* Cloud storage integration using Supabase Storage

---

## Architecture

```text
Client
   │
   ▼
React Frontend
   │
   ▼
Django REST API
   │
   ├── Authentication (JWT)
   ├── File Metadata
   ├── Sharing Service
   └── Storage Coordinator
            │
            ▼
      File Chunker
            │
            ▼
     Node Selection
            │
            ▼
 ┌─────────┬─────────┬─────────┬─────────┐
 │ Node A  │ Node B  │ Node C  │ Node D  │
 └─────────┴─────────┴─────────┴─────────┘
            │
            ▼
     Supabase Storage
```

---

## Tech Stack

### Frontend

* React
* Vite
* Axios

### Backend

* Django
* Django REST Framework
* Celery
* Simple JWT

### Database

* PostgreSQL
* Supabase PostgreSQL

### Storage

* Supabase Storage

### Messaging & Task Queue

* Redis

### Deployment

* Render
* Supabase


---

## Distributed Storage Workflow

### Upload

1. User uploads a file.
2. File is split into chunks.
3. Storage nodes are selected using a hashing strategy.
4. Multiple replicas are created for fault tolerance.
5. Chunks are stored in Supabase Storage.
6. Metadata is stored in PostgreSQL.

### Download

1. File metadata is retrieved.
2. Chunks are fetched from storage nodes.
3. Missing replicas are handled automatically.
4. Chunks are reassembled.
5. Original file is returned to the user.

### Fault Recovery

* Detects missing replicas.
* Restores replication factor automatically.
* Maintains storage redundancy.

### Rebalancing

* Redistributes chunks when storage topology changes.
* Ensures balanced storage utilization.

---

## Security Features

* JWT Authentication
* User-specific file ownership
* Password-protected share links
* Download limits
* Expiring share links
* Secure file access validation

---

## Current Status

### Implemented

* Authentication system
* File upload and download
* Share links
* Chunking and reassembly
* Replication
* Fault recovery
* Storage rebalancing
* Supabase integration
* Guest uploads
* Admin dashboard

### Planned

* Redis deployment
* Celery workers
* Celery Beat scheduler
* Multi-instance backend deployment
* Advanced analytics dashboard
* Real-time storage metrics

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/<username>/bitshare.git
cd bitshare
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SUPABASE_BUCKET=BitShare

DATABASE_URL=your_database_url

```

### Run Migrations

```bash
python manage.py migrate
```

### Create Admin User

```bash
python manage.py createsuperuser
```

### Start Backend

```bash
python manage.py runserver
```

### Start Frontend

```bash
npm install
npm run dev
```

---

## Key Distributed Systems Concepts Demonstrated

* File Chunking
* Data Replication
* Fault Tolerance
* Storage Rebalancing
* Distributed Storage Nodes
* Replica Recovery
* Consistent Data Reconstruction
* Cloud Object Storage Integration

---

## Live Demo

🚀 Frontend: https://bitshare-frontend-weld.vercel.app/

🔗 Backend API: https://bitshare-backend.onrender.com/

### Demo Credentials

You can create an account or use the guest upload feature to test the platform.


## Author

**Shaikh Md Zaid**


