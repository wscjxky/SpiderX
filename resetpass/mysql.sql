-- 危险操作，清空alarm表
TRUNCATE TABLE alarmrecord;
TRUNCATE TABLE realtimegroupdatarecord;
TRUNCATE TABLE groupdatarecord;
TRUNCATE TABLE realtimecelldatarecord;
TRUNCATE TABLE celldatarecord;
TRUNCATE TABLE recordlog;
-- 增加group_name字段
ALTER TABLE `realtimegroupdatarecord` ADD COLUMN `group_name` VARCHAR(50) NULL DEFAULT NULL AFTER `is_discharge`;
-- 增加group_name字段
ALTER TABLE `realtimecelldatarecord` ADD COLUMN `group_name` VARCHAR(50) NULL DEFAULT NULL AFTER `is_discharge`;
-- 增加group_name字段
ALTER TABLE `groupdatarecord` ADD COLUMN `group_name` VARCHAR(50) NULL DEFAULT NULL AFTER `is_discharge`;
-- 增加group_name字段
ALTER TABLE `alarmrecord` ADD COLUMN `group_name` VARCHAR(50) NULL DEFAULT NULL AFTER `remark`;



-- 增加id字段主键(耗时)
DELETE FROM realtimegroupdatarecord WHERE id IN ( SELECT id from  (select  id from realtimegroupdatarecord  group  by  id   having  COUNT(id) > 1) temp);
ALTER TABLE `realtimegroupdatarecord` ADD PRIMARY KEY ( `id` ) ;
DELETE FROM groupdatarecord WHERE id IN ( SELECT id from  (select  id from groupdatarecord  group  by  id   having  COUNT(id) > 1) temp);
ALTER TABLE `groupdatarecord` ADD PRIMARY KEY ( `id` ) ;

-- 同步3个月之后的数据到mysql

-- D:\tools\apache-tomcat-8.5.51\webapps\upsmanager\WEB-INF\classes\constant


-- ALTER TABLE "equipment" ADD COLUMN "isQueryTemperature" TINYINT NULL DEFAULT NULL  AFTER `resistance_threshold_value`;
