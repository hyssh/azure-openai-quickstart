USE [master]
GO
CREATE LOGIN [openaiuser] WITH PASSWORD=N'SAFEPASSWORD2023!@#'
GO
USE [wwidb]
GO
CREATE USER [openaiuser] FOR LOGIN [openaiuser] WITH DEFAULT_SCHEMA=[SalesLT]
GO
EXEC sp_addrolemember 'db_datareader', 'openaiuser'
EXEC sp_addrolemember 'db_datareader', 'openaiuser'