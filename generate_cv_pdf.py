#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DBA简历PDF生成器
使用ReportLab库生成标准格式的PDF简历
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import os
import platform

def create_cv_pdf():
    """生成刘力夫DBA简历PDF"""
    
    # 设置PDF输出路径
    pdf_path = "刘力夫_DBA_简历_CN_v3.pdf"
    
    # 创建PDF文档
    doc = SimpleDocTemplate(
        pdf_path, 
        pagesize=A4, 
        rightMargin=2*cm, 
        leftMargin=2*cm, 
        topMargin=2*cm, 
        bottomMargin=2*cm
    )
    
    # 获取样式表
    styles = getSampleStyleSheet()

    # 注册中文字体，解决中文显示为方块的问题
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

    # 定义样式
    styleN = styles["Normal"]
    styleN.fontName = "STSong-Light"
    styleN.fontSize = 10
    styleN.leading = 14
    
    # 标题样式
    styleH = ParagraphStyle(
        name="Heading",
        fontSize=13,
        leading=16,
        spaceAfter=10,
        spaceBefore=10,
        fontName="STSong-Light"
    )
    
    # 姓名标题样式
    styleName = ParagraphStyle(
        name="Name",
        fontSize=18,
        leading=22,
        spaceAfter=5,
        spaceBefore=5,
        fontName="STSong-Light",
        alignment=TA_CENTER
    )
    
    # 构建PDF内容
    content = [
        Paragraph("刘力夫（LIU Lifu）", styleName),
        Paragraph("男 | 40岁 | 电话：15810517437 | 邮箱：15810517437@139.com | 城市：北京", styleN),
        Paragraph("求职意向：高级DBA / 数据库运维工程师 / 数据库工程师 | 期望薪资：20K–40K | 18年工作经验", styleN),
        Spacer(1, 15),

        Paragraph("一、职业概述", styleH),
        Paragraph("拥有18年IT与运维经验，专注于MySQL / PostgreSQL / Oracle生产级运维与架构设计，长期承担高可用、备份恢复、性能优化与迁移割接工作。熟练Linux与脚本自动化，能以Prometheus/Grafana、Zabbix构建可观测与告警体系；熟悉云上RDS与跨地域容灾实践。具备流程规范化与应急演练能力，可支撑7x24关键业务稳定。", styleN),
        Spacer(1, 12),

        Paragraph("二、核心技能", styleH),
        Paragraph("• 数据库引擎：MySQL、PostgreSQL、Oracle、SQL Server、达梦<br/>"
                  "• 集群与高可用：MySQL MGR/InnoDB Cluster、Orchestrator/MHA、ProxySQL/PgBouncer；PostgreSQL 流复制/Patroni；Oracle DG/RAC；读写分离、分库分表<br/>"
                  "• 备份恢复与容灾：XtraBackup、pgBackRest/WAL-G、RMAN；跨机房/异地容灾；RTO/RPO 指标与恢复演练<br/>"
                  "• 性能优化：慢SQL治理、执行计划/索引/锁等待分析、分区/分片设计、容量与成本规划<br/>"
                  "• 自动化与规范：Python/Shell、自动巡检与健康评分、SQL审核、与CI/CD集成的数据库变更（Flyway/Liquibase）<br/>"
                  "• 监控与告警：Prometheus+Grafana、Zabbix、日志审计与可观测性建设<br/>"
                  "• 云与容器：Aliyun/AWS/Azure RDS，Aurora/PolarDB；Docker、Kubernetes<br/>"
                  "• 安全与合规：权限最小化、加密与脱敏、审计留痕；CSV/GxP/GMP", styleN),
        Spacer(1, 12),

        Paragraph("三、工作经历", styleH),
        Paragraph("<b>百济神州生物药业有限公司 — ITBP（数据库方向）</b><br/>2025.01 – 至今<br/>"
                  "负责Oracle / PostgreSQL / MySQL 生产环境规划与运维；建立标准化SOP。<br/>"
                  "落地高可用：MySQL InnoDB Cluster/Orchestrator，PostgreSQL Patroni 流复制，Oracle DG；实现读写分离。<br/>"
                  "备份与容灾：XtraBackup / pgBackRest / RMAN，制定RTO≤30min、RPO≤5min 并按月演练。<br/>"
                  "监控与自动化：Prometheus+Grafana+Alertmanager，Python/Shell 巡检与容量预测，SQL审核流程。<br/>"
                  "变更与迁移：接入CI/CD（Flyway/Liquibase）管理DDL变更与跨版本迁移，零中断/低窗口割接。<br/>"
                  "效果：关键系统P95时延下降30%+，资源成本下降15%+。", styleN),
        Spacer(1, 10),

        Paragraph("<b>苏州云数医药科技有限公司 — CSV验证工程师</b><br/>2023.10 – 2024.12<br/>"
                  "负责实验室系统（LIMS/ELN）数据库验证与合规性文件（URS/FAT/OQ/PQ）。<br/>"
                  "核查数据库配置、权限、日志、备份策略，确保GxP合规。<br/>"
                  "跨部门协调QA/QC/IT，实现系统快速验收与稳定运行。", styleN),
        Spacer(1, 10),

        Paragraph("<b>航天信息股份有限公司海外业务分公司 — 实施运维经理</b><br/>2018.10 – 2023.05<br/>"
                  "负责坦桑尼亚酒店税项目数据库接口与后台架构设计。<br/>"
                  "自主开发远程监控系统，实现海外项目自动化运维，年节省40万元成本。<br/>"
                  "管理私有云工具链项目，交付中间件平台及数据库支持服务。", styleN),
        Spacer(1, 10),

        Paragraph("<b>卓望信息技术（北京）有限公司 — 高级IT经理</b><br/>2014.05 – 2018.06<br/>"
                  "负责电力行业数据库系统建设与运维。<br/>"
                  "推行健康监测与补丁策略，保障系统连续可用性。<br/>"
                  "主导多个电力管理平台数据库设计，全部项目顺利验收。", styleN),
        Spacer(1, 10),

        Paragraph("<b>普华讯光（北京）科技有限公司 — 项目经理/主管</b><br/>2011.01 – 2014.05<br/>"
                  "带领项目组交付多地电力综合管理系统。<br/>"
                  "管理第三方团队，负责数据库部署、风险评估及性能测试。", styleN),
        Spacer(1, 12),

        Paragraph("四、教育背景", styleH),
        Paragraph("• 吉林大学 — 硕士 软件工程 (2010 – 2013)<br/>• 东北农业大学 — 本科 食品科学与工程 (2003 – 2007)", styleN),
        Spacer(1, 12),

        Paragraph("五、资格与认证", styleH),
        Paragraph("• Oracle 数据库专家认证（OCP）<br/>• 熟悉Aliyun RDS、AWS RDS、Azure SQL Database平台运维<br/>• AI辅助数据库分析与预测维护研究实践", styleN),
        Spacer(1, 12),

        Paragraph("六、项目与成就", styleH),
        Paragraph("• 高可用与容灾建设：设计并落地 MySQL MGR/Orchestrator、PostgreSQL Patroni、Oracle DG，异地容灾；RTO≤30min、RPO≤5min。<br/>"
                  "• 备份恢复与演练：XtraBackup/pgBackRest/RMAN 周期性恢复演练，月度演练通过率100%。<br/>"
                  "• 迁移与割接：完成多套跨版本/跨云迁移与读写切换，最小化停机窗口；性能优化使核心交易QPS提升20%+。", styleN),
        Spacer(1, 12),

        Paragraph("七、自我评价", styleH),
        Paragraph("拥有数据库深厚基础与云原生视角，兼具架构设计与实操经验。熟悉从传统数据库到云数据库平台转型的全过程。善于在企业环境中平衡性能、安全、合规与成本。未来职业目标：成为具备数据库平台化与智能化能力的资深DBA。", styleN)
    ]

    # 生成PDF
    doc.build(content)
    
    print(f"PDF简历已成功生成：{pdf_path}")
    return pdf_path

if __name__ == "__main__":
    create_cv_pdf()
