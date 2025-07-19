# 🚨 Alerting System Guide

## Overview

Your Calculator API now has a **production-grade alerting system** that monitors:
- **Error Rates** (400/500 responses)
- **Response Times** (slow performance)
- **API Availability** (service down)
- **High Load** (traffic spikes)
- **Database Issues** (operation errors)

## 🎯 Alert Types

### 1. High Error Rate Alert
- **Trigger**: Error rate > 5% for 2 minutes
- **Severity**: Warning
- **Action**: Check API logs and database connectivity

### 2. High Response Time Alert
- **Trigger**: 95th percentile response time > 0.5 seconds
- **Severity**: Warning
- **Action**: Investigate performance bottlenecks

### 3. API Down Alert
- **Trigger**: Service not responding for 30 seconds
- **Severity**: Critical
- **Action**: Immediate service restart required

### 4. High Request Rate Alert
- **Trigger**: > 50 requests per second for 2 minutes
- **Severity**: Info
- **Action**: Monitor for potential DDoS or traffic spikes

### 5. Database Connection Issues
- **Trigger**: > 0.1 database errors per second
- **Severity**: Warning
- **Action**: Check database connectivity and logs

## 🔧 Setting Up Alerts in Grafana

### Step 1: Access Grafana
1. Open http://localhost:3001
2. Login with `admin` / `admin`

### Step 2: Configure Alert Rules
1. Go to **Alerting** → **Alert Rules**
2. You should see the "Calculator API Alerts" folder
3. Click on individual alerts to view/modify

### Step 3: Set Up Notification Channels
1. Go to **Alerting** → **Notification channels**
2. Configure:
   - **Email**: For critical alerts
   - **Slack**: For team notifications
   - **Webhook**: For custom integrations

### Step 4: Test Alerts
1. Run the alert test script:
   ```bash
   python scripts/test_alerts.py
   ```
2. Check Grafana for firing alerts
3. Verify webhook notifications

## 📊 Alert Dashboard

### Viewing Alerts
1. **Alerting** → **Alert Rules**: See all configured alerts
2. **Alerting** → **Silences**: Manage alert silencing
3. **Alerting** → **Contact points**: Manage notifications

### Alert States
- **Pending**: Alert condition met, waiting for duration
- **Firing**: Alert is active and sending notifications
- **Resolved**: Alert condition no longer met

## 🧪 Testing the Alert System

### Manual Testing
```bash
# Generate errors to trigger alerts
python scripts/test_alerts.py

# Check alert webhook
curl http://localhost:8000/api/alerts/status

# Test webhook directly
curl -X POST http://localhost:8000/api/alerts/webhook \
  -H "Content-Type: application/json" \
  -d '{"alerts":[{"status":"firing","labels":{"alertname":"Test Alert"}}]}'
```

### Automated Testing
The alert test script generates:
1. **400 Errors**: Invalid requests
2. **500 Errors**: Server errors
3. **High Load**: Concurrent requests
4. **Webhook Tests**: Direct alert notifications

## 🔔 Notification Channels

### Email Alerts
- Configure SMTP settings in Grafana
- Send to: admin@example.com
- Used for: Critical alerts

### Slack Integration
- Webhook URL: Configure your Slack webhook
- Channel: #alerts
- Used for: Team notifications

### Webhook Integration
- Endpoint: http://localhost:8000/api/alerts/webhook
- Used for: Custom integrations, logging, ticketing

## 📈 Alert Metrics

### Key Metrics Monitored
```promql
# Error Rate
sum(rate(http_requests_total{status=~"4..|5.."}[5m])) / sum(rate(http_requests_total[5m]))

# Response Time
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Request Rate
sum(rate(http_requests_total[5m]))

# Database Errors
rate(calculator_operations_total{status="error"}[5m])
```

## 🛠️ Customizing Alerts

### Adding New Alerts
1. Edit `monitoring/grafana/provisioning/alerting/calculator-alerts.yml`
2. Add new alert rules
3. Restart Grafana: `docker-compose restart grafana`

### Alert Thresholds
- **Error Rate**: 5% (adjust based on your SLA)
- **Response Time**: 0.5s (adjust based on requirements)
- **Request Rate**: 50 RPS (adjust based on capacity)

### Alert Duration
- **Critical**: 30s (immediate action needed)
- **Warning**: 1-2m (investigation needed)
- **Info**: 2m (monitoring only)

## 🚀 Production Considerations

### Alert Fatigue Prevention
- Set appropriate thresholds
- Use different severity levels
- Implement alert grouping
- Set up alert silences for maintenance

### Escalation Policies
- **Level 1**: Automated restart
- **Level 2**: Team notification
- **Level 3**: Management escalation
- **Level 4**: Emergency response

### Integration Options
- **PagerDuty**: For on-call rotations
- **Jira**: For incident tickets
- **Slack**: For team communication
- **Email**: For management reports

## 📋 Best Practices

1. **Test Alerts Regularly**: Run test scripts weekly
2. **Monitor Alert Volume**: Avoid alert fatigue
3. **Document Runbooks**: Include resolution steps
4. **Review Thresholds**: Adjust based on performance
5. **Backup Notifications**: Multiple notification channels
6. **Alert Ownership**: Assign responsibility for each alert

## 🎉 Congratulations!

You now have a **production-ready alerting system** that will:
- ✅ **Detect Issues Early**: Before users are affected
- ✅ **Notify the Right People**: Based on severity
- ✅ **Provide Context**: With detailed descriptions
- ✅ **Enable Quick Response**: With actionable information
- ✅ **Prevent Downtime**: Through proactive monitoring

This is exactly how **enterprise applications** handle incident management! 🚀 