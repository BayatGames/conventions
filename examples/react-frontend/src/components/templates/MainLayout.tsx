import React from 'react';
import styled from '@emotion/styled';
import { useNavigate, useLocation } from 'react-router-dom';

// Organisms
import Header from '../organisms/Header';
import Footer from '../organisms/Footer';

// Define the prop types for the component
interface MainLayoutProps {
  children: React.ReactNode;
}

// Styled components
const MainContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
`;

const Content = styled.main`
  flex: 1;
  padding: 2rem 0;
`;

/**
 * MainLayout component
 * 
 * A template component that provides the basic page structure
 * with header, footer, and content area.
 */
const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();
  
  return (
    <MainContainer>
      <Header 
        onNavigate={(path) => navigate(path)}
        currentPath={location.pathname}
      />
      <Content className="container">
        {children}
      </Content>
      <Footer />
    </MainContainer>
  );
};

export default MainLayout; 