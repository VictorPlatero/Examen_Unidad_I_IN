# Publicacion en GitHub

Como `gh` no esta disponible en esta maquina, crear el repositorio remoto manualmente en GitHub y ejecutar:

```bash
git remote add origin https://github.com/<usuario>/<repositorio>.git
git branch -M main
git push -u origin main
```

Luego actualizar en `README.md`:

```text
URL GitHub del proyecto: https://github.com/<usuario>/<repositorio>
```

Configurar los secretos indicados en `docs/secrets.md` antes de ejecutar los workflows.
