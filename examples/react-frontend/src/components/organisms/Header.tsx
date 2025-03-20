import React from 'react';
import styled from '@emotion/styled';

// Molecules
import Navigation from '../molecules/Navigation';
import Logo from '../atoms/Logo';

// Define the prop types for the component
interface HeaderProps {
  onNavigate: (path: string) => void;
  currentPath: string;
}

// Styled components
const StyledHeader = styled.header`
  background-color: ${({ theme }) => theme.colors.background.paper};
  box-shadow: ${({ theme }) => theme.shadows.sm};
  padding: 1rem 0;
`;

const HeaderContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

/**
 * Header Component
 * 
 * Displays the site header with logo and navigation.
 */
const Header: React.FC<HeaderProps> = ({ onNavigate, currentPath }) => {
  const navItems = [
    { label: 'Home', path: '/' },
    { label: 'About', path: '/about' },
    { label: 'Dashboard', path: '/dashboard' },
  ];

  return (
    <StyledHeader>
      <HeaderContainer className="container">
        <Logo onClick={() => onNavigate('/')} />
        <Navigation 
          items={navItems}
          onNavigate={onNavigate}
          currentPath={currentPath}
        />
      </HeaderContainer>
    </StyledHeader>
  );
};

export default Header; 