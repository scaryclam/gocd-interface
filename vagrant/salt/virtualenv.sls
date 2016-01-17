gocd-interface_env:
  file.directory:
    - name: /virtualenv/gocd-interface
    - user: vagrant
    - group: vagrant
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

/virtualenv/gocd-interface:
  virtualenv.managed:
    - use_wheel : False
    - system_site_packages: False
    - requirements: /build/requirements.txt
    - user: vagrant

