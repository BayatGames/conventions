# Component Structure Standards

## Directory Organization

- Group components by feature or domain
- Use index files for cleaner imports
- Organize related components in subfolders

```plaintext
components/
├── users/
│   ├── UserList.tsx
│   ├── UserDetail.tsx
│   └── index.ts
├── auth/
│   ├── LoginForm.tsx
│   ├── RegisterForm.tsx
│   └── index.ts
└── common/
    ├── Button.tsx
    ├── Input.tsx
    └── index.ts
```

## Component File Structure

- Imports (grouped and ordered)
- Interface/Type definitions
- Component declaration
- Helper functions
- Styles (if co-located)
- Export statement

```typescript
// 1. External imports
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// 2. Internal imports
import { api } from '../../services/api';
import { Button } from '../common/Button';

// 3. Type definitions
interface IUserListProps {
  initialFilter?: string;
}

interface IUser {
  id: string;
  name: string;
  email: string;
}

// 4. Component implementation
export const UserList: React.FC<IUserListProps> = ({ initialFilter = '' }) => {
  const [users, setUsers] = useState<IUser[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchUsers();
  }, []);

  // 5. Helper functions
  const fetchUsers = async () => {
    setLoading(true);
    try {
      const data = await api.getUsers();
      setUsers(data);
    } catch (error) {
      console.error('Failed to fetch users:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUserClick = (userId: string) => {
    navigate(`/users/${userId}`);
  };

  return (
    <div className="user-list">
      {loading ? (
        <p>Loading users...</p>
      ) : (
        users.map((user) => (
          <div 
            key={user.id} 
            onClick={() => handleUserClick(user.id)}
          >
            <h3>{user.name}</h3>
            <p>{user.email}</p>
          </div>
        ))
      )}
    </div>
  );
};
```

## Component Types

- **Presentational Components**: Focus on UI, receive data via props
- **Container Components**: Focus on data and behavior
- **Higher-Order Components**: Enhance other components
- **Layout Components**: Structure the page

## Component Composition

- Favor composition over inheritance
- Use the children prop for flexible component patterns
- Create specialized components rather than adding complex props logic
- Extract reusable patterns into custom hooks
