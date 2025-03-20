import React from 'react';
import styled from '@emotion/styled';

// Atoms
import Heading from '../atoms/Heading';
import Text from '../atoms/Text';
import Button from '../atoms/Button';

// Styled components
const HomeContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2rem 0;
`;

const HeroSection = styled.section`
  margin-bottom: 4rem;
  max-width: 800px;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  justify-content: center;
  
  @media (max-width: 480px) {
    flex-direction: column;
    width: 100%;
    max-width: 300px;
  }
`;

const FeatureSection = styled.section`
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 2rem;
  margin-top: 2rem;
  
  @media (min-width: ${({ theme }) => theme.breakpoints.md}) {
    grid-template-columns: repeat(3, 1fr);
  }
`;

const FeatureCard = styled.div`
  background-color: ${({ theme }) => theme.colors.background.paper};
  padding: 2rem;
  border-radius: ${({ theme }) => theme.borderRadius.medium};
  box-shadow: ${({ theme }) => theme.shadows.sm};
  text-align: left;
`;

/**
 * Home Page Component
 * 
 * The landing page of the application.
 */
const HomePage: React.FC = () => {
  return (
    <HomeContainer>
      <HeroSection>
        <Heading level={1}>Welcome to Bayat React Frontend</Heading>
        <Text variant="body1" style={{ marginTop: '1rem' }}>
          A production-ready React application template demonstrating modern frontend 
          development practices and conventions.
        </Text>
        <ButtonGroup>
          <Button 
            variant="primary" 
            size="large"
            onClick={() => window.open('https://github.com/bayat/examples/react-frontend', '_blank')}
          >
            Get Started
          </Button>
          <Button 
            variant="outlined" 
            size="large"
            onClick={() => window.open('https://github.com/bayat/examples/react-frontend/docs', '_blank')}
          >
            Documentation
          </Button>
        </ButtonGroup>
      </HeroSection>
      
      <Heading level={2}>Key Features</Heading>
      <FeatureSection>
        <FeatureCard>
          <Heading level={3}>Component Architecture</Heading>
          <Text variant="body2">
            Built with atomic design principles, organizing components into atoms, 
            molecules, organisms, templates, and pages.
          </Text>
        </FeatureCard>
        <FeatureCard>
          <Heading level={3}>State Management</Heading>
          <Text variant="body2">
            Centralized state management with Redux Toolkit and React hooks
            for predictable state updates.
          </Text>
        </FeatureCard>
        <FeatureCard>
          <Heading level={3}>Type Safety</Heading>
          <Text variant="body2">
            Fully typed with TypeScript to catch errors during development
            and improve code quality.
          </Text>
        </FeatureCard>
      </FeatureSection>
    </HomeContainer>
  );
};

export default HomePage; 