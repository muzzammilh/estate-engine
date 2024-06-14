
# Estate Engine

## Introduction
The Estate Engine (PMS) is a comprehensive solution designed to facilitate the management of properties by various types of users including Admins, Owners, Maintainers, and Tenants. The system allows for efficient handling of property-related tasks, user profiles, billing, maintenance, and more.

## Features

### User Types
- **Admin**
- **Owner**
- **Maintainer**
- **Tenant**

### Admin Features
- **Profile Management**
  - Update profile
  - Change password
- **Manage Owners**
- **Version Update**
- **App Settings**
  - Update name, logo, location, etc.
- **System Settings**
  - Configure color scheme
  - Set language preferences
  - Define currency settings

### Owner Features
- **Profile Management**
  - Update profile
  - Change password
- **Property Management**
  - CRUD operations on properties and units
  - Own and lease properties
- **Tenant Management**
  - CRUD operations on tenants for properties and units
- **Billing**
  - Create invoices
  - Send notifications
  - Configure recurring settings
- **Expenses Management**
  - Track expenses by users (tenant, owner, maintainer)
- **Document Management**
  - Manage documents related to tenants
- **Property Information**
  - View detailed information about properties
- **Maintenance Management**
  - Add maintainers for properties
  - Request maintenance services
- **Tickets**
  - Handle tickets raised by tenants
  - Reply to tenant queries
- **Notice Board**
  - Post notices visible to all tenants of a property
- **Reports**
  - Generate earnings reports
  - Calculate profit and loss
  - Track expenses
  - Monitor maintenance activities
  - Generate tenant reports
- **Settings**
  - Configure payment gateway
  - Define expense types
  - Set tax settings
  - Customize invoice types
  - Define maintenance types
  - Configure ticket types

### Maintainer Features
- **Profile Management**
  - Update profile
  - Change password
- **Tickets Management**
  - Handle and reply to tickets
- **Maintenance Requests**
  - Update request status (done, in progress, etc.)
- **Property Information**
  - Access information about assigned properties

### Tenant Features
- **Profile Management**
  - Update profile
  - Change password
- **Invoices**
  - Pay invoices
  - Print invoices
- **Ticket Management**
  - Create tickets
  - Track actions taken by owners and maintainers
- **Property Information**
  - View information about the property
- **Maintenance Requests**
  - Submit maintenance requests
- **Document Management**
  - Upload documents for owner approval

## Implementation Progress

| Feature                          | Admin | Owner | Maintainer | Tenant | Status       |
|----------------------------------|-------|-------|------------|--------|--------------|
| Profile Management               | ✔️    | ✔️    | ✔️         | ✔️     | Completed    |
| Update Profile                   | ✔️    | ✔️    | ✔️         | ✔️     | Completed    |
| Change Password                  | ✔️    | ✔️    | ✔️        | ✔️     | In Progress  |
| Manage Owners                    | ✔️    |       |            |        | In Progress  |
| Version Update                   | ✔️    |       |            |        | In Progress  |
| App Settings                     | ✔️    |       |            |        | In Progress  |
| System Settings                  | ✔️    |       |            |        | In Progress  |
| Property Management              |       | ✔️    |            |        | In Progress  |
| CRUD Properties and Units        |       | ✔️    |            |        | In Progress  |
| Own and Lease Properties         |       | ✔️    |            |        | In Progress  |
| Tenant Management                |       | ✔️    |            |        | In Progress  |
| CRUD Tenants                     |       | ✔️    |            |        | In Progress  |
| Billing                          |       | ✔️    |            |        | In Progress  |
| Create Invoices                  |       | ✔️    |            |        | In Progress  |
| Send Notifications               |       | ✔️    |            |        | In Progress  |
| Recurring Settings               |       | ✔️    |            |        | In Progress  |
| Expense Management               |       | ✔️    |            |        | In Progress  |
| Track Expenses                   |       | ✔️    |            |        | In Progress  |
| Document Management              |       | ✔️    |            |        | In Progress  |
| Actions on Documents             |       | ✔️    |            |        | In Progress  |
| Property Information             |       | ✔️    | ✔️         | ✔️     | In Progress  |
| Maintenance Management           |       | ✔️    |            |        | In Progress  |
| Add Maintainers                  |       | ✔️    |            |        | In Progress  |
| Request Maintenance              |       | ✔️    |            |        | In Progress  |
| Tickets Management               |       | ✔️    | ✔️         | ✔️     | In Progress  |
| Handle Tickets                   |       | ✔️    | ✔️         | ✔️     | In Progress  |
| Reply to Tickets                 |       | ✔️    | ✔️         | ✔️     | In Progress  |
| Notice Board                     |       | ✔️    |            |        | In Progress  |
| Reports                          |       | ✔️    |            |        | In Progress  |
| Earnings Reports                 |       | ✔️    |            |        | In Progress  |
| Profit and Loss                  |       | ✔️    |            |        | In Progress  |
| Expense Reports                  |       | ✔️    |            |        | In Progress  |
| Maintenance Reports              |       | ✔️    |            |        | In Progress  |
| Tenant Reports                   |       | ✔️    |            |        | In Progress  |
| Settings                         |       | ✔️    |            |        | In Progress  |
| Payment Gateway                  |       | ✔️    |            |        | In Progress  |
| Expense Type                     |       | ✔️    |            |        | In Progress  |
| Tax Setting                      |       | ✔️    |            |        | In Progress  |
| Invoice Type                     |       | ✔️    |            |        | In Progress  |
| Maintenance Type                 |       | ✔️    |            |        | In Progress  |
| Ticket Type                      |       | ✔️    |            |        | In Progress  |
| Invoices                         |       |       |            | ✔️     | In Progress  |
| Pay Invoices                     |       |       |            | ✔️     | In Progress  |
| Print Invoices                   |       |       |            | ✔️     | In Progress  |
| Maintenance Requests             |       |       | ✔️         | ✔️     | In Progress  |
| Submit Maintenance Requests      |       |       | ✔️         | ✔️     | In Progress  |
| Document Management for Tenants  |       |       |            | ✔️     | In Progress  |
| Upload Documents                 |       |       |            | ✔️     | In Progress  |
| Actions on Documents by Owner    |       |       |            | ✔️     | In Progress  |

## Contributing
We welcome contributions from the community. Please read our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

---

Feel free to update the feature status and implementation progress as development continues. This README should provide a clear and organized overview of the Property Management System and its development status.
