import React from 'react';
import styled from '@emotion/styled';

// Define the prop types for the component
export interface ButtonProps {
  /**
   * Button variant
   */
  variant?: 'primary' | 'secondary' | 'outlined' | 'text';
  
  /**
   * Button size
   */
  size?: 'small' | 'medium' | 'large';
  
  /**
   * Optional icon
   */
  icon?: React.ReactNode;
  
  /**
   * Is the button full width
   */
  fullWidth?: boolean;
  
  /**
   * Is the button disabled
   */
  disabled?: boolean;
  
  /**
   * Button type attribute
   */
  type?: 'button' | 'submit' | 'reset';
  
  /**
   * Button children
   */
  children: React.ReactNode;
  
  /**
   * Click handler
   */
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  
  /**
   * Additional class names
   */
  className?: string;
}

// Helper function to get color based on variant
const getColorStyles = ({ variant = 'primary', theme }: { variant: ButtonProps['variant'], theme: any }) => {
  switch (variant) {
    case 'primary':
      return `
        background-color: ${theme.colors.primary.main};
        color: ${theme.colors.primary.contrastText};
        border: 1px solid ${theme.colors.primary.main};
        
        &:hover:not(:disabled) {
          background-color: ${theme.colors.primary.dark};
          border-color: ${theme.colors.primary.dark};
        }
      `;
    case 'secondary':
      return `
        background-color: ${theme.colors.secondary.main};
        color: ${theme.colors.secondary.contrastText};
        border: 1px solid ${theme.colors.secondary.main};
        
        &:hover:not(:disabled) {
          background-color: ${theme.colors.secondary.dark};
          border-color: ${theme.colors.secondary.dark};
        }
      `;
    case 'outlined':
      return `
        background-color: transparent;
        color: ${theme.colors.primary.main};
        border: 1px solid ${theme.colors.primary.main};
        
        &:hover:not(:disabled) {
          background-color: rgba(0, 0, 0, 0.04);
        }
      `;
    case 'text':
      return `
        background-color: transparent;
        color: ${theme.colors.primary.main};
        border: 1px solid transparent;
        
        &:hover:not(:disabled) {
          background-color: rgba(0, 0, 0, 0.04);
        }
      `;
    default:
      return '';
  }
};

// Helper function to get size styles
const getSizeStyles = ({ size = 'medium' }: { size: ButtonProps['size'] }) => {
  switch (size) {
    case 'small':
      return `
        padding: 0.4rem 0.75rem;
        font-size: 0.75rem;
      `;
    case 'large':
      return `
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
      `;
    case 'medium':
    default:
      return `
        padding: 0.6rem 1.25rem;
        font-size: 0.875rem;
      `;
  }
};

// Styled component
const StyledButton = styled.button<ButtonProps>`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-weight: 500;
  border-radius: ${({ theme }) => theme.borderRadius.medium};
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  line-height: 1.5;
  letter-spacing: 0.02em;
  
  ${props => getColorStyles(props)}
  ${props => getSizeStyles(props)}
  
  width: ${props => props.fullWidth ? '100%' : 'auto'};
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  &:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.5);
  }
`;

/**
 * Button Component
 * 
 * A versatile button component with different variants and sizes.
 */
const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'medium',
  icon,
  fullWidth = false,
  disabled = false,
  type = 'button',
  children,
  onClick,
  className,
  ...rest
}) => {
  return (
    <StyledButton
      variant={variant}
      size={size}
      fullWidth={fullWidth}
      disabled={disabled}
      type={type}
      onClick={onClick}
      className={className}
      {...rest}
    >
      {icon && <span className="button-icon">{icon}</span>}
      {children}
    </StyledButton>
  );
};

export default Button; 