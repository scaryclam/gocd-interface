goint_user:
  postgres_user.present:
    - name: goint_vagrant
    - password: vagrant
    - createdb: true
    - user: postgres
    - superuser: true

goint_db:
  postgres_database:
    - present
    - name: goint_vagrant
    - template: template1
    - user: postgres
