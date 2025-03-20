import React from 'react';
import styled from '@emotion/styled';

// Atoms
import Link from '../atoms/Link';

// Types
interface NavigationItem {
  label: string;
  path: string;
}

interface NavigationProps {
  items: NavigationItem[];
  onNavigate: (path: string) => void;
  currentPath: string;
}

// Styled components
const Nav = styled.nav`
  display: flex;
`;

const NavList = styled.ul`
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 1.5rem;
`;

const NavItem = styled.li<{ isActive: boolean }>`
  a {
    color: ${({ isActive, theme }) => 
      isActive ? theme.colors.primary.main : theme.colors.text.primary};
    font-weight: ${({ isActive, theme }) => 
      isActive ? theme.typography.fontWeightMedium : theme.typography.fontWeightRegular};
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      bottom: -4px;
      left: 0;
      width: ${({ isActive }) => isActive ? '100%' : '0'};
      height: 2px;
      background-color: ${({ theme }) => theme.colors.primary.main};
      transition: width 0.3s ease-in-out;
    }
    
    &:hover::after {
      width: 100%;
    }
  }
`;

/**
 * Navigation Component
 * 
 * Renders a horizontal navigation menu with active state indication.
 */
const Navigation: React.FC<NavigationProps> = ({ items, onNavigate, currentPath }) => {
  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>, path: string) => {
    e.preventDefault();
    onNavigate(path);
  };

  return (
    <Nav>
      <NavList>
        {items.map((item) => (
          <NavItem key={item.path} isActive={currentPath === item.path}>
            <Link 
              href={item.path} 
              onClick={(e) => handleClick(e, item.path)}
            >
              {item.label}
            </Link>
          </NavItem>
        ))}
      </NavList>
    </Nav>
  );
};

export default Navigation; 