# Django auth system
## About
App use custom and django tools to provide simple auth system based on roles and rights. First level depends on two types of roles: default and admin, second level depends on rights which are similar to http methods. Roles and rights determined in auth_app.models with many-to-many relation.
Permissons verification provided by decorators method, placed in auth_app.security.