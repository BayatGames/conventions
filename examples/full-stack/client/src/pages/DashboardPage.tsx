import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  CircularProgress,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  TextField,
  Checkbox,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import { RootState } from '../store';

// Mock data - would be replaced with API calls in a real app
const todoItems = [
  { id: '1', title: 'Complete dashboard UI', completed: true },
  { id: '2', title: 'Implement authentication', completed: true },
  { id: '3', title: 'Set up API routes', completed: false },
  { id: '4', title: 'Add error handling', completed: false },
  { id: '5', title: 'Deploy to production', completed: false },
];

const DashboardPage = () => {
  const { user } = useSelector((state: RootState) => state.auth);
  const [todos, setTodos] = useState(todoItems);
  const [newTodo, setNewTodo] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // In a real app, you would fetch the todos from the API
    setLoading(true);
    setTimeout(() => {
      setTodos(todoItems);
      setLoading(false);
    }, 500);
  }, []);

  const handleToggle = (id: string) => {
    setTodos(todos.map(todo => 
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  };

  const handleDelete = (id: string) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  const handleAddTodo = () => {
    if (newTodo.trim() === '') return;
    
    const newId = (Math.max(...todos.map(t => parseInt(t.id))) + 1).toString();
    setTodos([
      ...todos,
      { id: newId, title: newTodo, completed: false }
    ]);
    setNewTodo('');
  };

  const completedCount = todos.filter(t => t.completed).length;
  const pendingCount = todos.length - completedCount;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Typography variant="h6" color="textSecondary" paragraph>
        Welcome back, {user?.firstName || 'User'}!
      </Typography>
      
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              bgcolor: 'primary.light',
              color: 'white',
            }}
          >
            <Typography variant="h6" gutterBottom>
              Total Tasks
            </Typography>
            <Typography variant="h3">{todos.length}</Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              bgcolor: 'success.light',
              color: 'white',
            }}
          >
            <Typography variant="h6" gutterBottom>
              Completed
            </Typography>
            <Typography variant="h3">{completedCount}</Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              bgcolor: 'warning.light',
              color: 'white',
            }}
          >
            <Typography variant="h6" gutterBottom>
              Pending
            </Typography>
            <Typography variant="h3">{pendingCount}</Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              bgcolor: 'info.light',
              color: 'white',
            }}
          >
            <Typography variant="h6" gutterBottom>
              Completion Rate
            </Typography>
            <Typography variant="h3">
              {todos.length > 0
                ? `${Math.round((completedCount / todos.length) * 100)}%`
                : '0%'}
            </Typography>
          </Paper>
        </Grid>
      </Grid>
      
      <Paper sx={{ p: 2, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Task Management
        </Typography>
        
        <Box sx={{ display: 'flex', mb: 2 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Add a new task"
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
            sx={{ mr: 1 }}
          />
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleAddTodo}
            disabled={newTodo.trim() === ''}
          >
            Add
          </Button>
        </Box>
        
        <Divider sx={{ my: 2 }} />
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        ) : (
          <List>
            {todos.map((todo) => (
              <ListItem key={todo.id} divider>
                <Checkbox
                  edge="start"
                  checked={todo.completed}
                  onChange={() => handleToggle(todo.id)}
                />
                <ListItemText
                  primary={todo.title}
                  sx={{
                    textDecoration: todo.completed ? 'line-through' : 'none',
                    color: todo.completed ? 'text.disabled' : 'text.primary',
                  }}
                />
                <ListItemSecondaryAction>
                  <IconButton
                    edge="end"
                    aria-label="delete"
                    onClick={() => handleDelete(todo.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        )}
      </Paper>
    </Box>
  );
};

export default DashboardPage; 