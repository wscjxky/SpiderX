-- 注意使用原版的battery.config和server.xml,client.xml
-- 加入新告警
INSERT INTO "BatteryMonitoringSystem"."dbo"."AlarmType" ("alarm_type", "description") VALUES ('13', '请检查温度检测装置');
-------------------------
INSERT INTO "BatteryMonitoringSystem"."dbo"."AlarmType" ("alarm_type", "description") VALUES ('14', '网络通信断开');

-- 加入组名
ALTER TABLE "dbo"."AlarmRecord" ADD "group_name" VARCHAR(50) NULL DEFAULT NULL;
-------------------------
ALTER TABLE "dbo"."GroupDataRecord" ADD "group_name" VARCHAR(50) NULL DEFAULT NULL;



-- 新增查询温度字段
ALTER TABLE "dbo"."EquipmentConfiguration" ADD "isQueryTemperature" TINYINT  DEFAULT 1;

-- 新增查询温度字段
UPDATE "BatteryMonitoringSystem"."dbo"."EquipmentConfiguration" SET "isQueryTemperature"=1;

-- 分表（耗时）
CREATE TABLE "AlarmRecord_001" (
	"id" UNIQUEIDENTIFIER NOT NULL,
	"equip_id" INT NULL DEFAULT NULL,
	"group_no" INT NULL DEFAULT NULL,
	"cell_no" INT NULL DEFAULT NULL,
	"alarm_type" INT NULL DEFAULT NULL,
	"start_time" DATETIME NULL DEFAULT NULL,
	"end_time" DATETIME NULL DEFAULT NULL,
	"remark" NVARCHAR(50) NULL DEFAULT NULL,
	"group_name" VARCHAR(50) NULL DEFAULT NULL,
	PRIMARY KEY ("id")
);
-------------------------
insert into AlarmRecord_001 select * from  AlarmRecord WHERE end_time is not null  and not EXISTS( select * from  BatteryMonitoringSystem.dbo.AlarmRecord_001)   and datediff(DAY, start_time, GETDATE()) > 90;
-------------------------
DELETE FROM AlarmRecord  WHERE end_time is not null and datediff(DAY, start_time, GETDATE()) > 90 ;

-- 分电池库
CREATE TABLE "CellDataRecord_001" (
	"id" UNIQUEIDENTIFIER NOT NULL,
	"equip_id" INT NULL DEFAULT NULL,
	"group_no" INT NULL DEFAULT NULL,
	"cell_no" INT NULL DEFAULT NULL,
	"cell_voltage" DECIMAL(18,3) NULL DEFAULT NULL,
	"cell_resistance" DECIMAL(18,3) NULL DEFAULT NULL,
	"cell_contactResistance" DECIMAL(18,3) NULL DEFAULT NULL,
	"cell_temperature" DECIMAL(18,3) NULL DEFAULT NULL,
	"record_time" DATETIME NULL DEFAULT NULL,
	"discharge_identify" NCHAR(18) NULL DEFAULT NULL,
	"is_discharge" BIT NULL DEFAULT NULL,
	PRIMARY KEY ("id")
);
insert into CellDataRecord_001 select * from  CellDataRecord WHERE record_time is not null  and not EXISTS( select * from  BatteryMonitoringSystem.dbo.CellDataRecord_001)  and datediff(DAY, record_time, GETDATE()) > 90;
-------------------------
DELETE FROM CellDataRecord  WHERE record_time is not null and datediff(DAY, record_time, GETDATE()) > 90 ;

-- 分组数库
CREATE TABLE  "GroupDataRecord_001" (
	"id" UNIQUEIDENTIFIER NOT NULL,
	"equip_id" INT NULL DEFAULT NULL,
	"group_no" INT NULL DEFAULT NULL,
	"group_voltage" DECIMAL(18,3) NULL DEFAULT NULL,
	"group_current" DECIMAL(18,1) NULL DEFAULT NULL,
	"temperature" DECIMAL(18,1) NULL DEFAULT NULL,
	"average_resistance" DECIMAL(18,3) NULL DEFAULT NULL,
	"max_cell_voltage" DECIMAL(18,3) NULL DEFAULT NULL,
	"max_voltage_cellno" INT NULL DEFAULT NULL,
	"min_cell_voltage" DECIMAL(18,3) NULL DEFAULT NULL,
	"min_voltage_cellno" INT NULL DEFAULT NULL,
	"max_cell_resistance" DECIMAL(18,3) NULL DEFAULT NULL,
	"max_resistance_cellNo" INT NULL DEFAULT NULL,
	"min_cell_resistance" DECIMAL(18,3) NULL DEFAULT NULL,
	"min_resistance_cellno" INT NULL DEFAULT NULL,
	"record_time" DATETIME NULL DEFAULT NULL,
	"discharge_identify" NCHAR(18) NULL DEFAULT NULL,
	"is_discharge" BIT NULL DEFAULT NULL,
	"group_name" VARCHAR(50) NULL DEFAULT (NULL),
	PRIMARY KEY ("id")
);
insert into GroupDataRecord_001 select * from  GroupDataRecord WHERE record_time is not null and not EXISTS( select * from  BatteryMonitoringSystem.dbo.GroupDataRecord_001) and datediff(DAY, record_time, GETDATE()) > 90;
-------------------------
DELETE FROM GroupDataRecord  WHERE record_time is not null and datediff(DAY, record_time, GETDATE()) > 90 ;


-- 创建备份库（单独执行）
CREATE DATABASE "OldBatteryMonitoringSystem";

-- 创建完成后再执行下面的
USE "OldBatteryMonitoringSystem";
CREATE TABLE  "AlarmRecord" (
	"id" UNIQUEIDENTIFIER NOT NULL,
	"equip_id" INT NULL DEFAULT NULL,
	"group_no" INT NULL DEFAULT NULL,
	"cell_no" INT NULL DEFAULT NULL,
	"alarm_type" INT NULL DEFAULT NULL,
	"start_time" DATETIME NULL DEFAULT NULL,
	"end_time" DATETIME NULL DEFAULT NULL,
	"remark" NVARCHAR(50) NULL DEFAULT NULL,
	"group_name" VARCHAR(50) NULL DEFAULT NULL,
	PRIMARY KEY ("id")
);

-------------------------
CREATE TABLE "CellDataRecord" (
	"id" UNIQUEIDENTIFIER NOT NULL,
	"equip_id" INT NULL DEFAULT NULL,
	"group_no" INT NULL DEFAULT NULL,
	"cell_no" INT NULL DEFAULT NULL,
	"cell_voltage" DECIMAL(18,3) NULL DEFAULT NULL,
	"cell_resistance" DECIMAL(18,3) NULL DEFAULT NULL,
	"cell_contactResistance" DECIMAL(18,3) NULL DEFAULT NULL,
	"cell_temperature" DECIMAL(18,3) NULL DEFAULT NULL,
	"record_time" DATETIME NULL DEFAULT NULL,
	"discharge_identify" NCHAR(18) NULL DEFAULT NULL,
	"is_discharge" BIT NULL DEFAULT NULL,
	PRIMARY KEY ("id")
);

-------------------------
CREATE TABLE  "GroupDataRecord" (
	"id" UNIQUEIDENTIFIER NOT NULL,
	"equip_id" INT NULL DEFAULT NULL,
	"group_no" INT NULL DEFAULT NULL,
	"group_voltage" DECIMAL(18,3) NULL DEFAULT NULL,
	"group_current" DECIMAL(18,1) NULL DEFAULT NULL,
	"temperature" DECIMAL(18,1) NULL DEFAULT NULL,
	"average_resistance" DECIMAL(18,3) NULL DEFAULT NULL,
	"max_cell_voltage" DECIMAL(18,3) NULL DEFAULT NULL,
	"max_voltage_cellno" INT NULL DEFAULT NULL,
	"min_cell_voltage" DECIMAL(18,3) NULL DEFAULT NULL,
	"min_voltage_cellno" INT NULL DEFAULT NULL,
	"max_cell_resistance" DECIMAL(18,3) NULL DEFAULT NULL,
	"max_resistance_cellNo" INT NULL DEFAULT NULL,
	"min_cell_resistance" DECIMAL(18,3) NULL DEFAULT NULL,
	"min_resistance_cellno" INT NULL DEFAULT NULL,
	"record_time" DATETIME NULL DEFAULT NULL,
	"discharge_identify" NCHAR(18) NULL DEFAULT NULL,
	"is_discharge" BIT NULL DEFAULT NULL,
	"group_name" VARCHAR(50) NULL DEFAULT (NULL),
	PRIMARY KEY ("id")
);

-- 备份表（耗时）
USE "OldBatteryMonitoringSystem";
insert into OldBatteryMonitoringSystem.dbo.AlarmRecord select * from  BatteryMonitoringSystem.dbo.AlarmRecord_001 WHERE end_time is not null and not EXISTS( select * from  OldBatteryMonitoringSystem.dbo.AlarmRecord) and datediff(DAY, start_time, GETDATE()) > 367 ;
-------------------------
insert into OldBatteryMonitoringSystem.dbo.GroupDataRecord select * from  BatteryMonitoringSystem.dbo.GroupDataRecord_001 WHERE record_time is not null and not EXISTS( select * from  OldBatteryMonitoringSystem.dbo.GroupDataRecord) and  datediff(DAY, record_time, GETDATE()) > 367;
-------------------------
insert into OldBatteryMonitoringSystem.dbo.CellDataRecord select * from  BatteryMonitoringSystem.dbo.CellDataRecord_001 WHERE record_time is not null and not EXISTS( select * from  OldBatteryMonitoringSystem.dbo.CellDataRecord) and datediff(DAY, record_time, GETDATE()) > 367;

-------------------------
DELETE FROM BatteryMonitoringSystem.dbo.AlarmRecord_001  WHERE end_time is not null and datediff(DAY, start_time, GETDATE()) > 367;
-------------------------
DELETE FROM BatteryMonitoringSystem.dbo.GroupDataRecord_001  WHERE record_time is not null and datediff(DAY, record_time, GETDATE()) > 367;
-------------------------
DELETE FROM BatteryMonitoringSystem.dbo.CellDataRecord_001  WHERE record_time is not null and datediff(DAY, record_time, GETDATE()) > 367;



-- 把最初的电阻值记录
USE "BatteryMonitoringSystem";

delete from BatteryMonitoringSystem.dbo.OrigionalResistance;
-------------------------
INSERT INTO BatteryMonitoringSystem.dbo.OrigionalResistance  
SELECT
newid(),
equip_id,
group_no-1 AS group_no,
cell_no-1 AS cell_no,
cell_resistance 
FROM
	dbo.RealTimeCellDataRecord 
WHERE
	EXISTS ( SELECT MIN ( record_time ) AS record_time, equip_id, group_no,
	 cell_no FROM RealTimeCellDataRecord GROUP BY equip_id, group_no, cell_no )


-- 危险操作，清空realtim表
USE "BatteryMonitoringSystem";
-------------------------
TRUNCATE TABLE realtimegroupdatarecord
-------------------------
TRUNCATE TABLE realtimecelldatarecord
