schema {
    query :Query
    mutation :Mutation
}

scalar Time

% for enum in enums:
enum ${enum.name()} {
    % for value, comment in enum.values:
    ${value}  # ${comment}
    % endfor
}

% endfor

% for interface_name, req, resp in services:
input ${req.get_name()} {
    % for field in req.get_fields():

}


% endfor

input ChargeQueryInput {
    beginTime:Time
    endTime:Time
    userID:[Int!]
    projectID:[String!]
    jobID:[String!]
    regionID:[Int!]
    jobType:[String!]
    status:[String!]
}

type ChargeQueryOutput {
    userID:Int!
    projectID:String!
    jobID:String!
    jobType:String!
    jobDescription:String!
    rows:String!
    columnNames:[String!]!
    beginTime:Time!
    endTime:Time!
    regionID:Int!
}

type Query {
    # 查询计费信息
    chargeQuery(chargeQueryInput:ChargeQueryInput!):[ChargeQueryOutput]
    # 查询作业结果
    jobResult(jobID:String!):JobResultInfo
    # 查询作业信息，jobID为空则返回所有的作业信息
    jobInfoList(projectID:String!, jobID:String):[JobInfo]
    # 查询作业状态
    processingJobList(projectID:String!):[JobInfo]
    # 查询未通过的作业信息
    notPassJobList(projectID:String!):[JobInfo]
    # 查询等保存的作业信息
# pendingSaveJobList(projectID:String!):[JobInfo]
    # 查询已保存作业信息
# savedJobList(projectID:String!):[JobInfo]
    # 查询其它作业信息
    otherJobList(projectID:String!):[JobInfo]
    # 结果查询
    # resultInfo(resultID:String!):ResultInfo
    # 结果查询，resultID为空，则查询当前用户的所有结果信息
    # resultInfoList(resultID:String!):[ResultInfo]
    # 项目信息查询
    projectInfoList(projectID:String):[ProjectInfo]
    # 数据区信息查询
    regionInfoList():[RegionInfo]
    # 查询工作表依赖关系
    worktableRelation(jobID:String!):[WorkTableRelation]
    # 算法结果预览
    previewAlgorithm(
        algorithm: String!,                 # 算法
    ): AlgorithmResult                      # 结果
}

# FusiontableInfo
input FusiontableInfo {
    tableID:String!
    key:String!
}

type Mutation {
    # 创建作业
# createJob(projectID:String!, algorithmID:String, jobType:JobType!, worktableID:String, jobDescription:String, platformThrowIn:String,
#           timeThrowIn:Time, downloadType:DownLoadType, interfaceType:InterfaceType):JobInfo
    createCalculateJob(projectID:String!, algorithmID:String!, jobType:JobType!, resultJobType:JobType, interfaceType:InterfaceType, jobDescription:String, crontab:String!):JobInfo
    # 创建结果使用的作业
    createResultJob(projectID:String!, jobType:JobType!, worktableID:String!, jobDescription:String, interfaceType:InterfaceType):JobInfo

    # 创建数据融合作业，表A的数据如果出现在表B中，则保存下来
    createDataFusionJob(projectID:String!, fusiontableInfos:[FusiontableInfo!]!, jobDescription:String):JobInfo

    stopCrontabJob(jobID:String!):Ret

    startCrontabJob(jobID:String!):Ret

    # 删除作业
    deleteJob(jobID:String!):Ret
    # 创建项目
    createProject(projectName:String!, projectDescription:String):ProjectInfo
    # 更改项目名称
    changeProjectName(projectID:String!, projectName:String!):Ret
    # 更改项目描述
    changeProjectDescription(projectID:String!, projectDescription:String!):Ret
    # 结束项目
    finishProject(projectID:String!):Ret
    # 修改结果名称
    changeResultName(resultID:String!, resultName:String!):Ret
    # 修改结果备注
    changeResultComment(resultID:String!, resultComment:String!):Ret
    # 保存结果信息
    saveResultInfo(jobID:String!, resultID:String!, resultName:String!, resultDescription:String!, deadTime:Time!):Ret
    # 保存工作表
    addWorkTable(
        name: String!                  # 表名
        oldFields: [TableFieldInput]!     # 表列字段类型
        newFields: [TableFieldInput]!
        rowCount: Float!               # 记录数
        jobID: String!                 # 工作ID
        projectID: String!             # 项目ID
        projectName: String           # 项目名
        algorithmID: String!                # 算法ID
        algorithmName: String              # 算法名
        parentTableIDs: [String!]      # 父表ID列表
    ): Ret
    # 申请授权表
    applyAccreditTable(
        tableID: String!,                   # 表ID
        startTime: String!,                 # 授权开始时间
        endTime: String!,                   # 授权结束时间
        filters: [FilterRuleInput!],        # 数据过滤条件
    ): Ret!
}
type AlgorithmResult{
    result:String!
}
# jobInfo
type JobInfo {
    # 作业ID
    jobID:String!
    # 作业类型
    jobType:JobType!
    # 算法ID
    algorithmID:String!
    # 结果ID
    resultID:String!
    # 工作表
    worktableID:String!
    # 工作表
    worktableName:String!
    # 父表信息
    parentTables:[String!]
    # 引用工作表
    referenceWorktableName:[String!]!
    # 作业描述
    jobDescription:String
    # 创建时间
    createdTime:Time!
    # 更新时间
    updatedTime:Time!
    # 作业状态
    jobStatus:JobStatus!
    # 失败原因
    failReason:String!
    # 定时状态
    crontabEnabled:Boolean!
}
# 数据区
type RegionInfo {
    # 数据区ID
    regionID:Int!
    # 数据区名字
    name:String!
    # 数据区网关
    gatewayaddress:String!
}
enum FieldValueType {
    TINYINT
    SMALLINT
    INT
    BIGINT
    BOOLEAN
    FLOAT
    DOUBLE
    STRING
    BINARY
    TIMESTAMP
    DECIMAL
    CHAR
    VARCHAR
    DATE
}

input TableFieldInput {
    name: String!           # 列名
    type: FieldValueType!   # 类型
    desc: String            # 描述
    validValues: String     # 有效值json字符串
}
type Ret {
    success:Boolean!
}
type table_field {
    name:String!

}
type WorkTableRelation {
    tableName:String!
    depends:[String!]!
}

enum OperatorType {
    EQ          # =
    UNEQ        # !=
    LT          # <
    LE          # <=
    GT          # >
    GE          # >=
    IN          # in
    NotIN       # not in
}

# 授权过滤规则
input FilterRuleInput {
    columnName: String!                 # 列名
    condition: OperatorType!            # 条件
    conditionValues: String!            # 条件值
}
enum JobResultType {
    DOWNLOAD
    WORKTABLE
    INTERFACE
}

type JobResultInfo {
    # 结果类型
    Type:JobResultType!
    # 下载类型
    DownloadType:DownLoadType
    # 文件路径
    FilePath:String
    # 文件列表
    FileList:[String!]
    # 作业结果
    Result:String!
    # 算法
    Code:String!
    # 列数
    Columns:Int!
    # 行数
    Rows:Int!
}

type JobOverview {
    # 作业总数
    amount: Int!
    # 审核中的作业数量
    auditingAmount: Int!
}

type JobProfile {
    totalJob:Int!
    processing:Int!
    notPass:Int!
    passed:Int!
    others:Int!
}

enum ProjectStatusEnum {
  EnableProject
  DisableProject
}

type ProjectInfo {
    # 项目ID
    projectID:String!
    # 项目名称
    name:String!
    # 项目描述
    description:String!
    # 用户ID
    userID:Int!
    # 项目状态
    status:ProjectStatusEnum!
    # 创建时间
    createdTime:Time!
    # 开始时间
    startedTime:Time!
    # 结束时间
    deletedTime:Time!
    # 更新时间
    updatedTime:Time!
    # 作业概览
    jobOverview:JobOverview
    # 作业统计
    jobProfile:JobProfile

}
# 项目结果展示
type projectResultInfo {
    # 作业ID
    jobID:String!
    # 类型
    type:String!
    # 作业结果
    result:String!
}

# 结果信息
type ResultInfo {
    # 结果ID
    resultID:String!
    # 结果名称
    name:String!
    # 结果备注
    comment:String!
    # 作业ID
    jobID:String!
    # 结果记录数
    size:Int!
    # 结果状态
    status:JobStatus!
    # 结果创建时间
    createdTime:Time!
    # 结果使用时间
    resultUsedTime:Time!
}
