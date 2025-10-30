// Import necessary components and libraries for the React application
import { Toaster } from "@/components/ui/toaster"; // Toast notification system
import { Toaster as Sonner } from "@/components/ui/sonner"; // Sonner toast notification system
import { TooltipProvider } from "@/components/ui/tooltip"; // Tooltip component provider
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"; // React Query for data fetching and caching
import { BrowserRouter, Routes, Route } from "react-router-dom"; // React Router for navigation
import Index from "./pages/Index"; // Main application page
import NotFound from "./pages/NotFound"; // 404 Not Found page

// Create a new QueryClient instance for React Query
const queryClient = new QueryClient();

// Main application component
const App = () => (
  // Provide the QueryClient to the entire application
  <QueryClientProvider client={queryClient}>
    {/* Provide tooltip context to the application */}
    <TooltipProvider>
      <Toaster /> {/* Render the main Toaster component */}
      <Sonner /> {/* Render the Sonner Toaster component */}
      {/* Set up browser routing for the application */}
      <BrowserRouter>
        {/* Define application routes */}
        <Routes>
          {/* Route for the home page */}
          <Route path="/" element={<Index />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          {/* Catch-all route for any undefined paths */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App; // Export the App component as the default export
