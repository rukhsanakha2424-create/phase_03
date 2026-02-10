# Organify Frontend

A modern React-based frontend for the Organify todo application, built with Next.js 16+, TypeScript, and Tailwind CSS.

## Features

- User authentication with Better Auth
- JWT-based API requests
- Task CRUD operations
- Responsive design (mobile, tablet, desktop)
- Type-safe development with TypeScript
- Real-time form validation

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT
- **API Client**: Centralized HTTP wrapper with auto JWT injection
- **Linting**: ESLint

## Getting Started

### Prerequisites

- Node.js 18+ (LTS recommended)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local

# Update .env.local with your backend API URL and Better Auth config
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your_secret_key
```

### Development

```bash
# Run development server
npm run dev

# Open in browser
# http://localhost:3000
```

### Build

```bash
# Type check
npm run type-check

# Build for production
npm run build

# Start production server
npm start
```

### Linting

```bash
# Check for lint errors
npx eslint src/ --ext .ts,.tsx

# Fix lint errors
npx eslint src/ --ext .ts,.tsx --fix
```

## Project Structure

```
src/
├── app/                      # Next.js App Router
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Home page
│   ├── (auth)/               # Auth routes (separate layout)
│   │   ├── signup/
│   │   └── signin/
│   └── (dashboard)/          # Protected routes
│       ├── tasks/
│       └── profile/
├── components/               # React components
│   ├── auth/                 # Auth-related components
│   ├── tasks/                # Task-related components
│   ├── layout/               # Layout components
│   └── common/               # Reusable components
├── lib/                      # Core libraries
│   ├── auth/                 # Auth context and utilities
│   ├── api/                  # API client
│   ├── hooks/                # Custom React hooks
│   └── validation/           # Form validation
├── styles/                   # Global styles
├── utils/                    # Utility functions
└── public/                   # Static assets
```

## API Integration

The frontend communicates with the backend API using a centralized API client (`lib/api/client.ts`) that:
- Automatically injects JWT tokens in Authorization headers
- Handles 401 responses by redirecting to signin
- Parses JSON responses
- Provides consistent error handling

## Authentication Flow

1. User signs up/signs in via Better Auth
2. Backend issues JWT token
3. Token is stored in HttpOnly cookie (secure)
4. API client automatically includes token in requests
5. Backend validates token and returns user-specific data
6. UI updates based on auth state from context

## Environment Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_BASE_URL` | `http://localhost:8000` | Backend API base URL |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | `http://localhost:3000` | Better Auth endpoint |
| `BETTER_AUTH_SECRET` | `secret_key_123` | Shared secret for JWT signing |

## Development Guidelines

- Use TypeScript for type safety
- Follow the component structure (one component per file)
- Use custom hooks for state management (useAuth, useTasks)
- Validate all form inputs before submission
- Always extract user_id from auth context for API calls
- Follow the class names conventions for Tailwind

## Testing

```bash
# Run tests (when implemented)
npm test

# Run tests in watch mode
npm test -- --watch
```

## Deployment

1. Build the application: `npm run build`
2. Deploy to Vercel, Netlify, or your hosting provider
3. Set environment variables in hosting platform
4. Monitor for errors in application logs

## Contributing

- Create feature branches from `main`
- Make atomic commits
- Write descriptive commit messages
- Test changes locally before pushing
- Update this README for significant changes

## License

This project is part of the Organify Todo Application.
