# [CA] CUSTOMER AUTO TOOL BY JANE
Tool Auto Hỗ trợ hoạt động chăm sóc khách hàng.
## 1. PROJECT CHARTER

### 1.1 Thông tin dự án
- **Tên dự án**: ca_customer_auto_tool_by_Jane
- **Mã dự án**: CA-20260101
- **Ngày bắt đầu**: 02/01/2026
- **Thời gian dự kiến**: 100 ngày + 20 ngày backup
- **Ngày kết thúc dự kiến**: 01/04/2026

### 1.2 Mục tiêu dự án

#### Mục tiêu chính
- Kiểm tra trạng thái hoạt động của số phone (NAB/NKP)
- Kiểm tra trạng thái hoạt động Facebook của số phone
- Kiểm tra trạng thái hoạt động Zalo của số phone
- Tự động gửi tin nhắn theo kênh gửi, giờ gửi, nội dung gửi

#### Mục tiêu đo lường (KPIs)
- Xử lý được ≥100 số điện thoại trong 10 phút
- Uptime hệ thống ≥99%
- Error rate <5%

### 1.3 Phạm vi dự án

#### Trong phạm vi:
- Phân tích số điện thoại từ file Excel
- Kiểm tra trạng thái Zalo public
- Kiểm tra cài đặt riêng tư (tin nhắn/cuộc gọi)
- Gửi tin nhắn qua Zalo và SMS
- Thu thập thông tin bổ sung
- Xuất báo cáo Excel, plot image

#### Ngoài phạm vi:
- Giao diện web phức tạp
- Tích hợp database production
- Hệ thống thanh toán
- Mobile application

---

## 2. BUSINESS REQUIREMENTS DOCUMENT (BRD)

### 2.1 Tổng quan nghiệp vụ

#### Bối cảnh
Trong nghiệp vụ Chăm sóc khách hàng qua điện thoại, phone là kênh liên hệ chính của chúng ta, là kênh liên hệ hợp pháp duy nhất.

Để khai thác hiệu quả số phone, cần có tools hỗ trợ các thao tác manual để lọc thật nhanh nhóm khách hàng tiềm năng.

Bên cạnh đó là tự động các tác vụ theo kịch bản để thời gian Executive tập trung nghĩ ra cách optimize kịch bản.

### 2.2 Stakeholders

| Vai trò | Mô tả | Trách nhiệm |
|---------|-------|-------------|
| Product Owner | Người định hướng sản phẩm | Xác định yêu cầu, ưu tiên tính năng |
| Developer | Lập trình viên | Phát triển và maintain hệ thống |
| QA Tester | Kiểm thử viên | Đảm bảo chất lượng sản phẩm |
| End User | Người dùng cuối | Sử dụng hệ thống cho công việc |

### 2.3 Business Rules

#### Quy tắc xử lý dữ liệu
- Mỗi số điện thoại phải được validate trước khi xử lý
- Kết quả phân tích phải được lưu trữ với timestamp
- Data retention: 90 ngày cho dữ liệu phân tích, 7 ngày cho logs

#### Quy tắc gửi tin nhắn
- Không gửi quá 100 tin nhắn/phút để tránh spam
- Phải có cơ chế retry khi gửi thất bại (max 3 lần)
- Lưu trữ lịch sử gửi tin nhắn
- Không gửi tin nhắn ngoài giờ hành chính (8h-21h)

#### Quy tắc bảo mật
- Mã hóa thông tin nhạy cảm (AES-256)
- Log tất cả hoạt động quan trọng
- Không lưu trữ thông tin không cần thiết
- Tuân thủ PDPA (Personal Data Protection Act) của Việt Nam

---

## 3. FUNCTIONAL REQUIREMENTS SPECIFICATION

### 3.1 Use Cases

#### 3.1.1 UC-001: Phân tích số điện thoại Zalo từ Excel

**Tác nhân**: End User

**Mô tả**: Người dùng upload file Excel chứa danh sách số điện thoại, hệ thống phân tích và trả về kết quả.

**Luồng chính**:
1. Người dùng chọn file Excel input vào folder đã chỉ định
2. Hệ thống validate định dạng file .xlsx
3. Hệ thống đọc danh sách số điện thoại (cột `phone`)
4. Hệ thống validate & standardize từng số điện thoại về dạng (84, độ dài là 11 sau khi đã thêm đầu số 84)
5. Hệ thống kiểm tra trạng thái search tài khoản Zalo
6. Hệ thống kiểm tra cài đặt riêng tư (nhắn tin người lạ, gọi điện người lạ)
7. Hệ thống xuất data kết quả ra Excel (phone | available_to_search | status_message_stranger | status_call_stranger)
8. Hệ thống xuất kết quả tóm tắt ra hình .jpg
9. Người dùng tải file kết quả tại folder đã chỉ định

**Luồng ngoại lệ**:
- 2a. Không thấy file Excel -> Hiển thị lỗi
- 3a. Không thấy cột `phone` → Hiển thị lỗi
- 4a. Số điện thoại không hợp lệ → Standardize được thì chạy tiếp (status_standardize = 'standardized') || Không standardize được (ngoài rules) thì bỏ qua (status_process = 'ignore_due_to_invalid_phone_format')

#### 3.1.2 UC-002: Phân tích số điện thoại Facebook từ (pending)

**Tác nhân**: End User

**Mô tả**: Người dùng upload file Excel chứa danh sách số điện thoại, hệ thống phân tích và trả về kết quả.

**Luồng chính**:
1. Người dùng chọn file Excel input vào folder đã chỉ định
2. Hệ thống validate định dạng file .xlsx
3. Hệ thống đọc danh sách số điện thoại (cột `phone`)
4. Hệ thống validate từng số điện thoại về dạng (84, độ dài là 11 sau khi đã thêm đầu số 84)
5. Hệ thống kiểm tra trạng thái có tài khoản Facebook → Output: Link Facebook
6. Hệ thống kiểm tra trạng thái khóa trang cá nhân, khóa danh sách bạn bè
7. Hệ thống xuất data kết quả ra Excel (phone | link | name | user_name | status_feed | status_friend_list)
8. Hệ thống xuất kết quả tóm tắt ra hình .jpg
9. Người dùng tải file kết quả tại folder đã chỉ định

**Luồng ngoại lệ**:
- 3a. Không thấy cột `phone` → Hiển thị lỗi
- 4a. Số điện thoại không hợp lệ → Standardize hoặc bỏ qua

#### 3.1.3 UC-003: Gửi tin nhắn hàng loạt

**Tác nhân**: End User

**Mô tả**: Gửi tin nhắn đến danh sách số điện thoại theo lịch trình.

**Luồng chính**:
1. Người dùng upload file Excel chứa: số điện thoại, nội dung gửi chưa xử lý biến, kênh gửi, thời gian gửi
2. Hệ thống validate dữ liệu input
3. Hệ thống map message template với biến trong kho data
4. Hệ thống gửi tin nhắn theo lịch trình
5. Hệ thống xuất báo cáo kết quả
   - File: phone | sent_channel | sent_message | date_sent_schedule | date_sent_actual | sent_status
   - Visual summary

#### 3.1.4 UC-004: Thu thập thông tin bổ sung (pending)

**Tác nhân**: System

**Mô tả**: Tự động thu thập thông tin gia đình/cá nhân từ các nguồn công khai.

**Luồng chính**:
1. Hệ thống nhận danh sách số điện thoại
2. Hệ thống tìm kiếm thông tin trên các platform
3. Hệ thống trích xuất thông tin liên quan
4. Hệ thống lưu trữ thông tin đã thu thập
5. Hệ thống cập nhật profile contact

### 3.2 Functional Requirements Detail

#### 3.2.1 FR-001: Excel Import/Export
- FR-001.1: Hệ thống phải hỗ trợ import file Excel (.xlsx, .xls)
- FR-001.2: Hệ thống phải hỗ trợ export kết quả ra Excel, Plot

#### 3.2.2 FR-002: Phone Analysis
- FR-002.1: Hệ thống phải validate định dạng số điện thoại Việt Nam
- FR-002.2: Hệ thống phải kiểm tra trạng thái Zalo public/private
- FR-002.3: Hệ thống phải kiểm tra cài đặt nhắn tin người lạ
- FR-002.4: Hệ thống phải kiểm tra cài đặt gọi điện người lạ
- FR-002.5: Hệ thống phải hỗ trợ import file Excel (.xlsx, .xls)
- FR-002.6: Hệ thống phải hỗ trợ export kết quả ra Excel, Plot

#### 3.2.3 FR-003: Message Sending
- FR-003.1: Hệ thống phải hỗ trợ gửi tin nhắn qua Zalo
- FR-003.2: Hệ thống phải hỗ trợ gửi tin nhắn qua SMS
- FR-003.3: Hệ thống phải hỗ trợ lên lịch gửi tin nhắn
- FR-003.4: Hệ thống phải theo dõi trạng thái gửi tin nhắn
- FR-003.5: Hệ thống phải tự động map được message template
- FR-003.6: Hệ thống phải hỗ trợ retry mechanism

#### 3.2.4 FR-004: Information Collection
- FR-004.1: Hệ thống phải thu thập thông tin từ social media
- FR-004.2: Hệ thống phải trích xuất thông tin gia đình
- FR-004.3: Hệ thống phải lưu trữ thông tin đã thu thập
- FR-004.4: Hệ thống phải cập nhật thông tin định kỳ

---

## 4. NON-FUNCTIONAL REQUIREMENTS

### 4.1 Performance Requirements
- **NFR-001**: Hệ thống phải xử lý được tối thiểu 100 số điện thoại trong 10 phút
- **NFR-002**: Response time cho mỗi API call ≤3 giây
- **NFR-003**: Batch processing phải xử lý song song tối thiểu 10 requests

### 4.2 Reliability Requirements
- **NFR-004**: Hệ thống phải có mechanism retry khi API call thất bại (max 3 attempts với exponential backoff)
- **NFR-005**: Uptime ≥99% trong giờ làm việc
- **NFR-006**: Tự động recovery khi có lỗi không nghiêm trọng

### 4.3 Security Requirements
- **NFR-007**: Hệ thống phải log tất cả hoạt động quan trọng
- **NFR-008**: API keys phải được bảo vệ trong environment variables
- **NFR-009**: Mã hóa dữ liệu nhạy cảm bằng AES-256
- **NFR-010**: Implement rate limiting để tránh abuse
- **NFR-011**: Tuân thủ PDPA (Personal Data Protection Act) Việt Nam

### 4.4 Usability Requirements
- **NFR-012**: Hệ thống phải có CLI interface đơn giản
- **NFR-013**: Error messages phải rõ ràng và hướng dẫn cách khắc phục
- **NFR-014**: Kết quả output phải có format dễ đọc
- **NFR-015**: Cung cấp user manual và documentation đầy đủ

### 4.5 Maintainability Requirements
- **NFR-016**: Code phải follow PEP 8 standard
- **NFR-017**: Test coverage ≥80%
- **NFR-018**: Tất cả functions phải có docstrings
- **NFR-019**: Version control với Git

### 4.6 Scalability Requirements
- **NFR-020**: Hệ thống phải xử lý được tối đa 10,000 số điện thoại/batch
- **NFR-021**: Architecture phải cho phép horizontal scaling trong tương lai

---

## 5. SYSTEM ARCHITECTURE DOCUMENT

### 5.1 Kiến trúc tổng quan

```
┌──────────────────────────────────────────────────────────────┐
│                        USER LAYER                            │
│                    (Excel Input/Output)                      │
└───────────────────────────────┬──────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────┐
│                      APPLICATION LAYER                      │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│    │ Zalo Phone   │  │  Facebook    │  │   Message    │     │
│    │  Analyzer    │  │   Analyzer   │  │   Sender     │     │
│    └──────────────┘  └──────────────┘  └──────────────┘     │
│    ┌──────────────────────────────────────────────────┐     │
│    │                Information Collector             │     │
│    └──────────────────────────────────────────────────┘     │
└───────────────────────────────┬─────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────┐
│                         SERVICE LAYER                       │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│    │    Excel     │  │    Phone     │  │   Logger     │     │
│    │   Handler    │  │  Validator   │  │   Service    │     │
│    └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────────────┬─────────────────────────────┘
                                │                       
┌───────────────────────────────▼─────────────────────────────┐
│                       INTEGRATION LAYER                     │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│    │   Zalo API   │  │ Facebook API │  │   SMS API    │     │
│    └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Component Architecture

#### 5.2.1 Core Components (Application Components)

| Component | Chức năng | Input | Output | Dependencies |
|-----------|-----------|-------|--------|--------------|
| Zalo Phone Analyzer | Phân tích trạng thái Zalo của số điện thoại | List of phone numbers | Analysis results | Phone Validator, External APIs, Selenium |
| Facebook Phone Analyzer | Phân tích trạng thái Facebook của số điện thoại | List of phone numbers | Analysis results | Phone Validator, External APIs |
| Message Sender | Gửi tin nhắn hàng loạt | Message templates | Sending results | Zalo Selenium, 3rd Tool |
| Information Collector | Thu thập thông tin liên quan của số điện thoại | List of phone numbers | Collected information | Social Media APIs |

#### 5.2.2 Service Components

| Component | Chức năng | Rules | Input | Output | Libraries | Features |
|-----------|-----------|-------|-------|--------|-----------|----------|
| Excel Handler | Xử lý file Excel (read/write) | - | Excel files | Dataframes/Excel files | pandas, openpyxl | read, write, validate |
| Phone Validator | Validate/Standardize format số điện thoại | Đầu số: 84, Độ dài số: 10 | List of phone numbers | Valid/Invalid status, Formatted phone | phonenumbers, re | validate, standardize |
| Logger Service | Logging và monitoring | Log levels, Retention policy | Events/Errors | Log files | logging, loguru | info, error, debug |

### 5.3 Data Flow Architecture

#### 5.3.1 Zalo Analysis Flow
```
Excel Input → Excel Handler → Phone Validator → Zalo Account Status Check 
→ Zalo Privacy Settings Check → Result Aggregator → Excel Output + Visual Report
```

#### 5.3.2 Facebook Analysis Flow
```
Excel Input → Excel Handler → Phone Validator → Facebook Search 
→ Profile Check → Privacy Check → Result Aggregator → Excel Output + Visual Report
```

#### 5.3.3 Message Sending Flow
```
Excel Input → Excel Handler → Validation → Message template mapping -> Schedule Manager → Message Queue → Channel Router (Zalo/SMS) → Delivery Tracker 
→ Result Logger → Report Generator
```

### 5.4 Technology Stack

#### 5.4.1 Core Technologies
- **Language**: Python 3.10+
- **Framework**: CLI-based application
- **Package Manager**: pip/poetry

#### 5.4.2 Key Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| pandas | 2.1.0+ | Data manipulation |
| openpyxl | 3.1.0+ | Excel handling |
| selenium | 4.15.0+ | Browser automation |
| requests | 2.31.0+ | HTTP requests |
| phonenumbers | 8.13.0+ | Phone validation |
| python-dotenv | 1.0.0+ | Environment variables |
| loguru | 0.7.0+ | Advanced logging |
| schedule | 1.2.0+ | Task scheduling |
| matplotlib | 3.8.0+ | Data visualization |
| cryptography | 41.0.0+ | Data encryption |

#### 5.4.3 Development Tools
- **Version Control**: Git
- **Testing**: pytest, unittest
- **Code Quality**: pylint, black, flake8
- **Documentation**: Sphinx

### 5.5 Database Design (File-based Storage)

```
/data
  /input          # Excel input files
  /output         # Result files, Generated reports
  /logs           # Application logs
  /cache          # Temporary cache
/src              # Source code
  /core           # Application Components
  /services       # Service Components
```

---

## 6. SECURITY & COMPLIANCE

### 6.1 Data Privacy & Protection

#### 6.1.1 PDPA Compliance (Vietnam)
- **Data Minimization**: Chỉ thu thập dữ liệu cần thiết
- **Purpose Limitation**: Sử dụng dữ liệu đúng mục đích
- **Storage Limitation**: Lưu trữ tối đa 90 ngày cho dữ liệu phân tích
- **Data Subject Rights**: Người dùng có quyền yêu cầu xóa dữ liệu

#### 6.1.2 Data Security Measures

**Encryption**:
```python
# AES-256 encryption for sensitive data
from cryptography.fernet import Fernet

# Key management
KEY_LOCATION = os.getenv('ENCRYPTION_KEY_PATH')
```

**Access Control**:
- File permissions: Read/Write chỉ cho user được authorize
- API keys stored in `.env` file (không commit vào Git)
- Sensitive logs được encrypt

### 6.2 Security Best Practices

1. **Input Validation**: Sanitize tất cả input từ Excel
2. **Rate Limiting**: Maximum 100 requests/minute
3. **Error Handling**: Không expose sensitive info trong error messages
4. **Secure Communication**: HTTPS cho tất cả API calls
5. **Audit Trail**: Log tất cả operations với timestamp và user ID

---

## 7. ERROR HANDLING & LOGGING

### 7.1 Error Handling Strategy

#### 7.1.1 Error Categories

| Error Level | Description | Action |
|-------------|-------------|--------|
| CRITICAL | System failure | Stop execution, alert admin |
| ERROR | Operation failed | Log error, retry if applicable |
| WARNING | Unexpected situation | Log warning, continue execution |
| INFO | Normal operation | Log for tracking |
| DEBUG | Detailed information | Log for development only |

#### 7.1.2 Retry Mechanism

```python
def retry_with_backoff(func, max_attempts=3, base_delay=1):
    """
    Retry function with exponential backoff
    Delays: 1s, 2s, 4s
    """
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
```

### 7.2 Logging Strategy

#### 7.2.1 Log Format
```
[TIMESTAMP] [LEVEL] [MODULE] [FUNCTION] - MESSAGE
2026-01-02 10:30:45 | INFO | phone_analyzer | validate_phone | Processing phone: 84901234567
```

#### 7.2.2 Log Levels Usage
- **DEBUG**: Chi tiết từng bước xử lý
- **INFO**: Các operations thành công
- **WARNING**: Validation failures, retry attempts
- **ERROR**: API failures, processing errors
- **CRITICAL**: System crashes, security breaches

#### 7.2.3 Log Retention Policy
- **Application Logs**: 30 ngày
- **Error Logs**: 90 ngày
- **Audit Logs**: 365 ngày
- **Debug Logs**: 7 ngày

#### 7.2.4 Log Storage
```
/logs
  /debug (dev env only)
    - debug_2026-01-02.log
  /info
    - info_2026-01-02.log
  /warning
    - warning_2026-01-02.log
  /error
    - error_2026-01-02.log
  /critical
    - critical_2026-01-02.log
  /app
    - app_2026-01-02.log
  /audit
    - audit_2026-01-02.log
```

---

## 8. TESTING STRATEGY

### 8.1 Test Levels

#### 8.1.1 Unit Testing
- **Coverage Target**: ≥80%
- **Framework**: pytest
- **Scope**: Individual functions and methods

**Test Cases**:
```
TC-001: Test phone validation with valid Vietnamese number
TC-002: Test phone validation with invalid format
TC-003: Test Excel import with valid file
TC-004: Test Excel import with missing columns
TC-005: Test standardization logic
```

#### 8.1.2 Integration Testing
- **Framework**: pytest
- **Scope**: Component interactions

**Test Scenarios**:
```
TS-001: End-to-end Zalo analysis flow
TS-002: End-to-end Facebook analysis flow
TS-003: Message sending with scheduling
TS-004: Error handling in API calls
```

#### 8.1.3 User Acceptance Testing (UAT)
- **Duration**: 2 ngày
- **Participants**: End Users, Product Owner

**UAT Checklist**:
- [ ] Import Excel file thành công
- [ ] Phân tích Zalo chính xác
- [ ] Phân tích Facebook chính xác
- [ ] Gửi tin nhắn theo schedule
- [ ] Export kết quả đúng format
- [ ] Visual reports dễ đọc

### 8.2 Test Data

#### 8.2.1 Sample Data Sets
```
/test_data
  - valid_phones.xlsx (100 valid numbers)
  - invalid_phones.xlsx (50 invalid numbers)
  - mixed_phones.xlsx (mix of valid/invalid)
  - large_dataset.xlsx (1000+ numbers for performance test)
```

#### 8.2.2 Test Scenarios

| Scenario ID | Description | Expected Result |
|-------------|-------------|-----------------|
| TS-001 | Valid phone numbers | All processed successfully |
| TS-002 | Invalid formats | Standardized or ignored |
| TS-003 | Empty file | Error message displayed |
| TS-004 | Missing phone column | Error message displayed |
| TS-005 | Large dataset (1000+) | Processed within time limit |

### 8.3 Performance Testing

#### 8.3.1 Load Testing
- **Tool**: locust or custom script
- **Metrics**: 
  - Throughput: requests/second
  - Response time: average, p95, p99
  - Error rate: percentage

#### 8.3.2 Performance Benchmarks
- 100 phones in ≤10 minutes
- Memory usage ≤2GB
- CPU usage ≤80%

---

## 9. DEPLOYMENT & OPERATIONS

### 9.1 Deployment Strategy

#### 9.1.1 Environment Setup

**Development Environment**:
```bash
# Prerequisites
- Python 3.10+
- pip or poetry
- Git

# Installation
git clone [repository]
cd collection-auto
pip install -r requirements.txt
cp .env.example .env
# Configure .env with API keys
```

**Production Environment**:
- Same as development
- Additional: Logging to centralized location
- Scheduled tasks via cron

#### 9.1.2 Configuration Management

**.env file structure**:
```
# API Keys
ZALO_API_KEY=your_key_here
FACEBOOK_API_KEY=your_key_here
SMS_API_KEY=your_key_here

# Encryption
ENCRYPTION_KEY_PATH=/path/to/key

# Logging
LOG_LEVEL=INFO
LOG_PATH=/var/log/collection-auto

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=100

# Paths
INPUT_FOLDER=./data/input
OUTPUT_FOLDER=./data/output
```

### 9.2 Monitoring & Alerting

#### 9.2.1 Key Metrics to Monitor

| Metric | Threshold | Alert Action |
|--------|-----------|--------------|
| Error Rate | >5% | Email alert |
| Processing Time | >15 min for 100 phones | Email alert |
| API Failure Rate | >10% | Immediate alert |
| Disk Space | <10% free | Warning alert |
| Memory Usage | >90% | Warning alert |

#### 9.2.2 Health Check
```python
def system_health_check():
    """
    Perform system health check
    Returns: dict with status of each component
    """
    return {
        "excel_handler": "OK",
        "phone_validator": "OK",
        "api_connections": "OK",
        "disk_space": "OK"
    }
```

### 9.3 Backup & Recovery

#### 9.3.1 Backup Strategy
- **Input Files**: Backup before processing
- **Output Files**: Keep for 90 days
- **Logs**: Keep for retention period
- **Configuration**: Version controlled in Git

#### 9.3.2 Disaster Recovery Plan
1. **Data Loss**: Restore from backup
2. **System Crash**: Restart service, check logs
3. **API Failures**: Switch to backup API if available
4. **Corruption**: Re-process from original input

---

## 10. MAINTENANCE & SUPPORT

### 10.1 Maintenance Schedule

| Task | Frequency | Description |
|------|-----------|-------------|
| Log Cleanup | Weekly | Remove old logs per retention policy |
| Performance Review | Monthly | Analyze performance metrics |
| Security Patch | As needed | Update dependencies |
| Backup Verification | Monthly | Test backup restoration |
| Documentation Update | Quarterly | Update based on changes |

### 10.2 Support Process

#### 10.2.1 Issue Tracking
- Use GitHub Issues or Jira
- Categories: Bug, Enhancement, Question
- Priority: Critical, High, Medium, Low

#### 10.2.2 SLA (Service Level Agreement)

| Priority | Response Time | Resolution Time |
|----------|---------------|-----------------|
| Critical | 1 hour | 4 hours |
| High | 4 hours | 24 hours |
| Medium | 1 day | 3 days |
| Low | 3 days | 1 week |

### 10.3 Change Management

#### 10.3.1 Change Process
1. Submit change request
2. Impact analysis
3. Approval from Product Owner
4. Implementation in dev environment
5. Testing
6. Deployment to production
7. Post-deployment verification

---

## 11. USER MANUAL

### 11.1 Installation Guide

```bash
# Step 1: Clone repository
git clone [repository-url]
cd collection-auto

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Configure environment
cp .env.example .env
nano .env  # Edit with your API keys

# Step 4: Verify installation
python main.py --version
```

### 11.2 Usage Examples

#### 11.2.1 Zalo Analysis
```bash
# Place your Excel file in data/input/
# File must have 'phone' column

python main.py analyze-zalo --input data/input/phones.xlsx

# Output: data/output/zalo_results_YYYYMMDD_HHMMSS.xlsx
```

#### 11.2.2 Facebook Analysis
```bash
python main.py analyze-facebook --input data/input/phones.xlsx

# Output: data/output/facebook_results_YYYYMMDD_HHMMSS.xlsx
```

#### 11.2.3 Send Messages
```bash
# Prepare Excel with columns: phone, message, channel, schedule_time
python main.py send-messages --input data/input/messages.xlsx

# Send immediately
python main.py send-messages --input data/input/messages.xlsx --immediate

# Output: data/output/message_results_YYYYMMDD_HHMMSS.xlsx
```

### 11.3 Input File Format

#### 11.3.1 Zalo Phone Analysis Input
```
Required columns:
- phone: Phone number (any format, will be standardized)

Example:
phone          
0901234567     
84912345678   
```

#### 11.3.2 Message Sending Input
```
Required columns:
- phone: Phone number
- message_template: Message content with <variables>
- sent_message: Message content with variable be mapped
- sent_channel: zalo or sms
- datet_sent_schedule: YYYY-MM-DD HH:MM (optional, send immediately if empty)

Example:
phone          | message_template               | sent_message                   | sent_channel | datet_sent_schedule
0901234567     | Hello <customer_name> from XYZ | Hello Nguyen Kim Ngan from XYZ | zalo    | 2026-01-03 09:00
84912345678    | Payment reminder               | Payment reminder               | sms     | 2026-01-03 10:00
```

### 11.4 Output File Format

#### 11.4.1 Zalo Phone Analysis Output
```
Columns:
- phone: Standardized phone number
- status_search: FOUND/STR_UNVALID_SEARCH_NUM_PHONE,...
- zalo_name: Name on Zalo
- zalo_avatar_link: Link avatar Zalo
- note: note for unexpected data or system error
- retry_count: Number of retry
- datet_checked: Checking at timestamp
```

#### 11.4.2 Facebook Analysis Output (pending)
```
Columns:
- phone: Standardized phone number
- status_standardize: standardized/ignore
- link: Facebook profile URL
- name: Profile name
- user_name: Username/handle
- status_feed: public/private/unknown
- status_friend_list: public/private/unknown
- last_checked: Timestamp
- error_message: Error details (if any)
```

#### 11.4.3 Message Sending Output
```
Columns:
- phone: Phone number
- sent_channel: zalo/sms
- sent_message: Message content (truncated)
- datet_sent_schedule: Scheduled time
- datet_sent_actual: Actual sent time
- sent_status: success/failed/pending
- error_message: Error details (if failed)
- retry_count: Number of retry attempts
```

### 11.5 Troubleshooting

#### 11.5.1 Common Issues

**Issue: "Column 'phone' not found in Excel file"**
```
Solution:
1. Check if your Excel file has a column named exactly "phone" (case-sensitive)
2. Make sure the column name has no extra spaces
3. The phone column should be in the first sheet
```

**Issue: "All phones marked as 'ignore'"**
```
Solution:
1. Check phone number format
2. Valid formats: 0901234567, 84901234567, +84901234567
3. Phone length must be 10 digits (excluding country code)
```

**Issue: "API connection failed"**
```
Solution:
1. Check internet connection
2. Verify API keys in .env file
3. Check if APIs are accessible (not blocked by firewall)
4. Review logs in /logs/error/ for details
```

**Issue: "Rate limit exceeded"**
```
Solution:
1. System is processing too many requests
2. Wait 1 minute and retry
3. Reduce batch size in configuration
4. Check rate limiting settings in .env
```

**Issue: "Permission denied when writing output"**
```
Solution:
1. Check folder permissions
2. Make sure output folder exists
3. Close Excel file if it's open
4. Run with appropriate user permissions
```

#### 11.5.2 Log Location
```
Application logs: /logs/app/app_YYYY-MM-DD.log
Error logs: /logs/error/error_YYYY-MM-DD.log
Debug logs: /logs/debug/debug_YYYY-MM-DD.log
```

#### 11.5.3 Getting Help
```
1. Check logs for error details
2. Search documentation for similar issues
3. Contact support team with:
   - Error message
   - Input file (sample)
   - Log file excerpt
   - Steps to reproduce
```

---

## 12. API DOCUMENTATION

### 12.1 Internal APIs

#### 12.1.1 Phone Validator API

```python
from services.phone_validator import PhoneValidator

validator = PhoneValidator()

# Validate single phone
result = validator.validate("0901234567")
# Returns: {
#   "is_valid": True,
#   "standardized": "84901234567",
#   "country_code": "84",
#   "local_number": "901234567"
# }

# Validate batch
results = validator.validate_batch(["0901234567", "0912345678"])
```

#### 12.1.2 Excel Handler API

```python
from services.excel_handler import ExcelHandler

handler = ExcelHandler()

# Read Excel
df = handler.read_excel("input.xlsx", required_columns=["phone"])

# Write Excel
handler.write_excel(df, "output.xlsx")

# Generate visual report
handler.generate_visual_report(df, "report.jpg")
```

#### 12.1.3 Zalo Analyzer API

```python
from analyzers.zalo_analyzer import ZaloAnalyzer

analyzer = ZaloAnalyzer()

# Analyze single phone
result = analyzer.analyze_phone("84901234567")
# Returns: {
#   "status_search": "found",
#   "status_message": "allowed",
#   "status_call": "blocked",
#   "zalo_name": "Nguyen Van A"
# }

# Analyze batch
results = analyzer.analyze_batch(phone_list)
```

#### 12.1.4 Message Sender API

```python
from services.message_sender import MessageSender

sender = MessageSender()

# Send via Zalo
result = sender.send_zalo(
    phone="84901234567",
    message="Hello",
    schedule_time=None  # Send immediately
)

# Send via SMS
result = sender.send_sms(
    phone="84901234567",
    message="Hello"
)

# Schedule message
result = sender.schedule_message(
    phone="84901234567",
    message="Hello",
    channel="zalo",
    schedule_time="2026-01-03 09:00"
)
```

### 12.2 External API Integration

#### 12.2.1 Zalo API Integration

**Endpoint**: `https://api.zalo.me/v2/user/info`

**Authentication**: Bearer token in .env

**Rate Limit**: 100 requests/minute

**Request Example**:
```python
headers = {
    "Authorization": f"Bearer {ZALO_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "phone": "84901234567"
}

response = requests.post(url, headers=headers, json=payload)
```

**Response Example**:
```json
{
  "error": 0,
  "message": "Success",
  "data": {
    "user_id": "1234567890",
    "display_name": "Nguyen Van A",
    "avatar": "https://...",
    "is_sensitive": false
  }
}
```

#### 12.2.2 Facebook API Integration

**Endpoint**: `https://graph.facebook.com/v18.0/search`

**Authentication**: Access token in .env

**Rate Limit**: 200 calls/hour/user

**Request Example**:
```python
params = {
    "q": "84901234567",
    "type": "user",
    "access_token": FACEBOOK_API_KEY
}

response = requests.get(url, params=params)
```

#### 12.2.3 SMS API Integration

**Endpoint**: `https://api.sms-provider.com/v1/send`

**Authentication**: API key in header

**Rate Limit**: 50 requests/minute

**Request Example**:
```python
headers = {
    "X-API-Key": SMS_API_KEY
}

payload = {
    "to": "84901234567",
    "message": "Hello",
    "sender": "COLLECT"
}

response = requests.post(url, headers=headers, json=payload)
```

---

## 13. GLOSSARY

### 13.1 Technical Terms

| Term | Definition |
|------|------------|
| **API** | Application Programming Interface - giao diện lập trình ứng dụng |
| **Batch Processing** | Xử lý hàng loạt nhiều items cùng lúc |
| **CLI** | Command Line Interface - giao diện dòng lệnh |
| **Exponential Backoff** | Kỹ thuật tăng thời gian chờ theo cấp số nhân khi retry |
| **Rate Limiting** | Giới hạn số requests trong một khoảng thời gian |
| **Retry Mechanism** | Cơ chế thử lại khi operation thất bại |
| **Sanitization** | Làm sạch dữ liệu input để tránh injection attacks |