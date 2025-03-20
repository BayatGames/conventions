import React from 'react';
import styled from '@emotion/styled';

// Atoms
import Text from '../atoms/Text';
import Link from '../atoms/Link';

// Styled components
const StyledFooter = styled.footer`
  background-color: ${({ theme }) => theme.colors.background.paper};
  box-shadow: ${({ theme }) => theme.shadows.sm};
  padding: 2rem 0;
  margin-top: auto;
`;

const FooterContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  
  @media (min-width: ${({ theme }) => theme.breakpoints.md}) {
    flex-direction: row;
    justify-content: space-between;
  }
`;

const FooterLinks = styled.div`
  display: flex;
  gap: 1.5rem;
  margin-top: 1rem;
  
  @media (min-width: ${({ theme }) => theme.breakpoints.md}) {
    margin-top: 0;
  }
`;

/**
 * Footer Component
 * 
 * Displays the site footer with copyright and links.
 */
const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <StyledFooter>
      <FooterContainer className="container">
        <Text variant="body2">
          © {currentYear} Bayat. All rights reserved.
        </Text>
        <FooterLinks>
          <Link href="/terms">Terms</Link>
          <Link href="/privacy">Privacy</Link>
          <Link href="/help">Help</Link>
          <Link href="/contact">Contact</Link>
        </FooterLinks>
      </FooterContainer>
    </StyledFooter>
  );
};

export default Footer; 