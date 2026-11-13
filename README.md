# SQL-PY JOIN

Proyecto de practica para reforzar conceptos de SQL Server y Python, con enfoque futuro en una aplicacion SaaS.

## Proposito

Este repositorio servira como base de aprendizaje incremental para:

- Practicar modelado y carga de datos en SQL Server.
- Documentar ejemplos de joins y relaciones entre tablas.
- Integrar posteriormente Python para consultas, automatizacion y APIs.
- Evolucionar el aprendizaje hacia patrones utiles para un futuro producto SaaS.

## Estado actual

El proyecto contiene un script SQL ya ejecutado para crear y poblar una tabla de referencia sobre tipos de joins.

<!-- (kommiBo) Rollback prevents persistence; it does not make the script read-only. -->
El valor versionado de `@EjecutarCommit` es `N`: el flujo normal revierte la transacción.
Aun en ese modo, el script ejecuta creación o borrado de filas, cambios de constraints e
inserciones dentro de la transacción antes del rollback. Puede adquirir bloqueos; no es
una consulta de sólo lectura ni un sandbox para una base persistente.

Si cambias explícitamente el valor a `Y`, el flujo normal confirma esos cambios y deja
creada o vaciada y recargada `dbo.REGISTER_JOIN`. Usa una instancia desechable autorizada,
revisa la base y el modo antes de ejecutar, y verifica el estado final además de los mensajes.
Consulta los [límites de uso](TERMS.md) y la [validación desechable](docs/validation-guide.md).

## Contrato externo

`SP_CreateTables.sql` requiere SQL Server, una base llamada `PYDB` y una tabla existente `dbo.REGISTER` con estas columnas: `INTERNAL_NUM`, `SCRIPT_NAME`, `SCRIPT_TYPE`, `ACTIVE`, `USER_STAMP`, `PROCESS_STAMP` y `DATE_TIME_STAMP`. La validación desechable crea ese contrato con `INTERNAL_NUM = 7` para `SP_CreateTables`.

El bloque `CATCH` revierte la transacción y devuelve el detalle del error como result set, pero no vuelve a lanzar la excepción. Por ello, los consumidores no deben interpretar únicamente el exit code como prueba de éxito; también deben verificar el estado esperado de la base.

## Validar

Requisitos: Bash, Docker y acceso para descargar la imagen oficial de SQL Server fijada en el validator.

```bash
bash tests/validate_sql.sh
```

El validator usa un contenedor efímero, comprueba el rollback predeterminado, ejecuta una copia temporal en modo commit dos veces y verifica filas, claves y recarga idempotente. El contenedor y la contraseña aleatoria se eliminan al salir.

El runtime aislado de kommiBo puede ejecutar las mismas comprobaciones sin acceso a Docker. Debe proporcionar `KOMMIBO_SQL_SERVER=sqlserver,1433`, una contraseña efímera en `KOMMIBO_SQL_PASSWORD` y el cliente `/opt/mssql-tools18/bin/sqlcmd`. El comando sigue siendo `bash tests/validate_sql.sh`. Este modo sólo admite ese sidecar desechable: crea `PYDB` y sus datos de prueba; el runtime conserva la responsabilidad de destruir el sidecar. El validator no elimina contenedores externos. No uses una base persistente ni una contraseña personal.

Las pruebas locales del transporte usan comandos simulados y no acreditan ejecución SQL:

```bash
python3 -m unittest discover -s tests -p 'test_validate_sql.py'
```

El workflow `Validation` ejecuta SQL real por ambos transportes: Docker y el cliente nativo del sidecar, conservando el mismo check requerido `validation`. El validator agrega `GO` al flujo enviado para despachar el último batch incluso cuando el archivo original no termina en una nueva línea; no modifica el archivo SQL. La prueba del sidecar también exige que SQL inválido termine con un código distinto de cero.

## Alcance futuro

El repositorio podra crecer con ejercicios y componentes relacionados con:

- Conexion Python a SQL Server.
- Consultas parametrizadas y validacion de datos.
- Automatizacion de cargas o reportes.
- APIs con FastAPI.
- Fundamentos reutilizables para una plataforma SaaS.

## Nota

Este es un proyecto de practica y evolucion tecnica. El codigo se mantendra simple, legible y orientado a aprendizaje aplicado.

## Licencia

El script SQL, validadores, ejemplos, configuración de workflow y notas técnicas
listados expresamente en [LICENSE](LICENSE) están disponibles bajo la licencia
[MIT](LICENSES/MIT.txt), incluidos sus permisos de uso comercial. El alcance no
incluye los runtimes externos ni material no listado; el aviso de procedencia AEKR
conserva su alcance separado.

## Gobernanza

Los cambios siguen el flujo de ingeniería AEKR: alcance acotado, validación determinista en infraestructura desechable, revisión mediante pull request y recuperación mediante revert PR. El autor y el revisor son actores técnicos distintos bajo una sola autoridad HOC; el revisor aprueba y fusiona el head exacto validado. Esta separación es un control operativo, no una auditoría independiente.


<!-- (kommiBo) Source-backed documentation navigation. -->
## Engineering recipes

See the [engineering notes](docs/engineering-notes/README.md) for reproducible examples, source references and validation limits.

<!-- (kommiBo) Project-specific behavior, privacy and permission boundaries. -->
## Privacy, use and permissions

El script es material educativo para una instancia desechable de SQL Server.
El rollback predeterminado no sustituye aislamiento ni autorización sobre la base.
Los stamps y resultados SQL también son datos: revisa logs y exports antes de publicarlos.
Las ideas SaaS son alcance futuro; no hay un servicio SaaS implementado aquí.

- [Privacy notice](PRIVACY.md): project processing, hosting and requests.
- [Use and service boundaries](TERMS.md): intended use and license precedence.
- [Licensing inventory](docs/licensing.md): project, dependency and AEKR provenance scopes.
- [Data handling](docs/data-handling.md): local artifacts and publication checks.
- [Security reporting](SECURITY.md): private reports and support limits.

<!-- (kommiBo) Route contributors to project-specific evidence and permission requirements. -->
See [CONTRIBUTING.md](CONTRIBUTING.md) for reproducible reports, validation scope and review evidence.

---

Built with the **[AI Engineering Knowledge Racking (AEKR)](https://aekr.io)** workflow.
