import React from 'react';
import { Routes, Route } from 'react-router-dom';

// Pages
import HomePage from './components/pages/Home';
import AboutPage from './components/pages/About';
import DashboardPage from './components/pages/Dashboard';
import NotFoundPage from './components/pages/NotFound';

// Templates
import MainLayout from './components/templates/MainLayout';

// Global styles
import GlobalStyles from './theme/GlobalStyles';

const App: React.FC = () => {
  return (
    <>
      <GlobalStyles />
      <MainLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </MainLayout>
    </>
  );
};

export default App; 