--**Script to create tables for SQL-PY JOIN project

--define la base a usar
use PYDB;

--commit switch
declare @EjecutarCommit char(1) = 'N'; --Cambia a 'Y' cuando esté Ok

begin try
    begin tran;

--Crea la tabla
        if OBJECT_ID('dbo.REGISTER_JOIN', 'U') is null
        begin
        create table dbo.REGISTER_JOIN
            (
            INTERNAL_REG_NUM int identity(1,1) not null primary key,
            INTERNAL_NUM int not null,
            JOIN_NAME nvarchar(50) not null,
            JOIN_DIRECTION nvarchar(50) not null,
            JOIN_NOTES nvarchar(200),
            ACTIVE char(1) not null,
            USER_STAMP nvarchar(50),
            PROCESS_STAMP nvarchar(200),
            DATE_TIME_STAMP datetime not null
            );
        end
        else
        begin 
            delete from dbo.REGISTER_JOIN;
        end;

--inserta el registro de tu tabla
        if not exists (select 1 from dbo.REGISTER where INTERNAL_NUM = 7)
        begin
            insert into dbo.REGISTER
                (
                    SCRIPT_NAME,
                    SCRIPT_TYPE,
                    ACTIVE,
                    USER_STAMP,
                    PROCESS_STAMP,
                    DATE_TIME_STAMP
                )
            values
                (
                    'SP_CreateTables',
                    'SQL',
                    'Y',
                    'ED',
                    'MANUAL_LOAD',
                    GETDATE()
                );
            end;

--crea el constraint con la tabla principal
        if not exists (
            select 1 from sys.objects
            where name = 'UQ_REGISTER_INTERNAL_NUM'
            and parent_object_id = OBJECT_ID('dbo.REGISTER')
                )
        begin 
            alter table dbo.REGISTER --crea el UNIQUE
            add constraint UQ_REGISTER_INTERNAL_NUM
            unique (INTERNAL_NUM);
        end;

        if not exists (
            select 1 from sys.objects
            where name = 'REG_001'
            and parent_object_id = OBJECT_ID('dbo.REGISTER_JOIN')
                )
        begin
            alter table dbo.REGISTER_JOIN --crea el FK
            add constraint REG_001
            foreign key (INTERNAL_NUM)
            references dbo.REGISTER(INTERNAL_NUM);
        end;

--Inserta los valores en la nueva tabla
            declare @InternalNum int;
            set @InternalNum = (
                select INTERNAL_NUM 
                from dbo.REGISTER 
                where SCRIPT_NAME = 'SP_CreateTables'
                and INTERNAL_NUM is not null
                );
            
            insert into dbo.REGISTER_JOIN
                (
                    INTERNAL_NUM,
                    JOIN_NAME,
                    JOIN_DIRECTION,
                    JOIN_NOTES,
                    ACTIVE,
                    USER_STAMP,
                    PROCESS_STAMP,
                    DATE_TIME_STAMP
                )
            values
                    (@InternalNum,'JOIN','Both Tables Matching Rows Only','Shorthand for INNER JOIN that returns only rows with matching values in both tables excluding non-matching records.','Y','ED','INITIAL_LOAD',getdate()),
                    (@InternalNum,'INNER JOIN','Both Tables Matching Rows Only','Returns only rows with matching values in both tables making it the standard join for related data retrieval.','Y','ED','INITIAL_LOAD',getdate()),
                    (@InternalNum,'LEFT JOIN','Left Table All Rows','Returns all rows from the left table and matching right rows filling unmatched right columns with NULL.','Y','ED','INITIAL_LOAD',getdate()),
                    (@InternalNum,'RIGHT JOIN','Right Table All Rows','Returns all rows from the right table and matching left rows filling unmatched left columns with NULL.','Y','ED','INITIAL_LOAD',getdate()),
                    (@InternalNum,'FULL OUTER JOIN','Both Tables All Rows','Returns all rows from both tables matching where possible and filling missing values with NULL.','Y','ED','INITIAL_LOAD',getdate()),
                    (@InternalNum,'CROSS JOIN','Both Tables All Combinations','Returns the Cartesian product of both tables generating every possible row combination without a join condition.','Y','ED','INITIAL_LOAD',getdate()),
                    (@InternalNum,'SELF JOIN','Same Table','Joins a table to itself using aliases to compare or relate rows within the same table such as hierarchies.','Y','ED','INITIAL_LOAD',getdate()),
                    (@InternalNum,'CROSS APPLY','Left Table Matching Rows Only','Executes a correlated subquery or table-valued function per left row returning only rows where the applied query returns results.','Y','ED','INITIAL_LOAD',getdate()),
                    (@InternalNum,'OUTER APPLY','Left Table All Rows','Executes a correlated subquery or table-valued function per left row returning all left rows and NULL when no result exists.','Y','ED','INITIAL_LOAD',getdate());

--valida visualmente tablas
        select * from dbo.REGISTER where INTERNAL_NUM = @InternalNum;
        select * from dbo.REGISTER_JOIN;

--Commit Switch validador
        if @EjecutarCommit = 'Y' 
        begin 
            commit;
        print 'Script commited - no errors';
        end 
        else 
        begin
            rollback; 
            print 'Script Rolled Back by Commit Switch';
        end;

--Transaction Catch validador
end try
begin catch 
    if @@TRANCOUNT > 0
    begin 
        rollback;
       print 'Script Rolled Back - Check errors';
    end 
    else 
    begin 
        print 'Script Failed - No open transaction';
    end;

--SQL error catch
select
        error_number()    as ErrorNumber,
        error_severity()    as Severity,
        error_state()       as State,
        error_line()         as ErrorLine,
        error_procedure() as ProcedureName,
        error_message()   as ErrorMessage;

end catch;