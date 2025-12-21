# CV Wizard Frontend

React + TypeScript + Vite frontend for CV Wizard application.

## Features

- 🎨 Modern UI with shadcn/ui components
- 📤 Drag-and-drop file upload
- 🤖 AI-powered CV analysis
- 📊 Interactive results display
- ⬇️ Download optimized CVs
- 📱 Mobile responsive

## Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

## Development

The app will be available at `http://localhost:5173`

Make sure the backend API is running at `http://localhost:8000`

## Project Structure

```
src/
├── components/
│   ├── ui/              # shadcn/ui components
│   ├── FileUpload.tsx   # File upload with drag-and-drop
│   └── CVAnalysis.tsx   # CV analysis results
├── lib/
│   ├── api.ts           # API client
│   └── utils.ts         # Utilities
├── App.tsx              # Main app component
├── main.tsx             # Entry point
└── index.css            # Global styles
```

## Technologies

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **shadcn/ui** - UI components
- **Axios** - HTTP client
- **React Dropzone** - File upload
- **React Markdown** - Markdown rendering
