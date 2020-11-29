db.auth('admin-user', 'admin-password')

db = db.getSiblingDB('lqdm')

db.createUser({
  user: 'lqdm',
  pwd: 'lqdm',
  roles: [
    {
      role: 'readWrite',
      db: 'lqdm',
    },
  ],
});