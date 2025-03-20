#!/bin/sh

# Run migrations
npx prisma migrate dev --name init

# Seed the database if needed
# npx prisma db seed

echo "Database initialization completed" 