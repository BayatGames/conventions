import React from 'react';
import { Global, css } from '@emotion/react';
import { theme } from './index';

const GlobalStyles: React.FC = () => (
  <Global
    styles={css`
      /* CSS Reset */
      *, *::before, *::after {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
      }

      /* Document */
      html {
        font-size: 16px;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-size-adjust: 100%;
      }

      body {
        font-family: ${theme.typography.fontFamily};
        font-size: ${theme.typography.fontSize}px;
        line-height: 1.5;
        color: ${theme.colors.text.primary};
        background-color: ${theme.colors.background.default};
      }

      /* Typography */
      h1, h2, h3, h4, h5, h6 {
        margin-bottom: 0.5em;
        font-weight: ${theme.typography.fontWeightBold};
        line-height: 1.2;
      }
      
      h1 {
        font-size: ${theme.typography.h1.fontSize};
      }
      
      h2 {
        font-size: ${theme.typography.h2.fontSize};
      }
      
      h3 {
        font-size: ${theme.typography.h3.fontSize};
      }
      
      h4 {
        font-size: ${theme.typography.h4.fontSize};
      }
      
      h5 {
        font-size: ${theme.typography.h5.fontSize};
      }
      
      h6 {
        font-size: ${theme.typography.h6.fontSize};
      }

      p {
        margin-bottom: 1rem;
      }

      a {
        color: ${theme.colors.primary.main};
        text-decoration: none;
        transition: color 0.2s ease-in-out;
        
        &:hover {
          color: ${theme.colors.primary.dark};
          text-decoration: underline;
        }
      }

      /* Images */
      img {
        max-width: 100%;
        height: auto;
      }

      /* Form Elements */
      button, input, optgroup, select, textarea {
        font-family: inherit;
        font-size: 100%;
        line-height: 1.15;
      }

      button {
        cursor: pointer;
      }

      /* Accessibility */
      .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border-width: 0;
      }

      /* Container */
      .container {
        width: 100%;
        padding-right: 1rem;
        padding-left: 1rem;
        margin-right: auto;
        margin-left: auto;
        
        @media (min-width: ${theme.breakpoints.sm}) {
          max-width: 540px;
        }
        
        @media (min-width: ${theme.breakpoints.md}) {
          max-width: 720px;
        }
        
        @media (min-width: ${theme.breakpoints.lg}) {
          max-width: 960px;
        }
        
        @media (min-width: ${theme.breakpoints.xl}) {
          max-width: 1140px;
        }
      }
    `}
  />
);

export default GlobalStyles; 