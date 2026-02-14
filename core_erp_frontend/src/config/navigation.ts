import {
  LayoutDashboard,
  Users,
  UserPlus,
  ClipboardList,
  CalendarDays,
  Plane,
  Laptop,
  UserMinus,
  BriefcaseBusiness,
  FolderKanban,
  Package,
  Wrench,
  FileCheck2,
  Receipt,
  HandCoins,
  Store,
  ShoppingCart,
  CreditCard,
  BarChart3,
} from "lucide-react";

export type Role = "ADMIN" | "HR" | "MANAGER" | "EMPLOYEE";

export type NavItem = {
  label: string;
  href: string;
  icon: any;
  roles: Role[];
};

export type NavGroup = {
  group: string;
  icon: any;
  roles: Role[];
  items: NavItem[];
};

export const NAV_TOP: NavItem[] = [
  {
    label: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
    roles: ["ADMIN", "HR", "MANAGER", "EMPLOYEE"],
  },
];

export const NAV_GROUPS: NavGroup[] = [
  {
    group: "Employees",
    icon: Users,
    roles: ["ADMIN", "HR"],
    items: [
      {
        label: "Employee Registration",
        href: "/employees/register",
        icon: UserPlus,
        roles: ["ADMIN", "HR"],
      },
      {
        label: "Performance Appraisal",
        href: "/employees/performance-appraisal",
        icon: ClipboardList,
        roles: ["ADMIN", "HR"],
      },
      {
        label: "Add Attendance",
        href: "/employees/attendance",
        icon: CalendarDays,
        roles: ["ADMIN", "HR"],
      },
      {
        label: "Employee Onsite Travel",
        href: "/employees/onsite-travel",
        icon: Plane,
        roles: ["ADMIN", "HR"],
      },
      {
        label: "Employee Assets",
        href: "/employees/assets",
        icon: Laptop,
        roles: ["ADMIN", "HR"],
      },
      {
        label: "Relieve Employee",
        href: "/employees/relieve-employee",
        icon: UserMinus,
        roles: ["ADMIN", "HR"],
      },
    ],
  },

  {
    group: "Clients",
    icon: BriefcaseBusiness,
    roles: ["ADMIN", "HR", "MANAGER"],
    items: [
      {
        label: "Client Registration",
        href: "/clients/client-registration",
        icon: FileCheck2,
        roles: ["ADMIN", "HR", "MANAGER"],
      },
    ],
  },

  {
    group: "Projects",
    icon: FolderKanban,
    roles: ["ADMIN", "HR", "MANAGER"],
    items: [
      {
        label: "Project Registration",
        href: "/projects/project-registration",
        icon: FolderKanban,
        roles: ["ADMIN", "HR", "MANAGER"],
      },
      {
        label: "Bill of Material",
        href: "/projects/bom",
        icon: Package,
        roles: ["ADMIN", "HR", "MANAGER"],
      },
      {
        label: "Project Commissioning",
        href: "/projects/commissioning",
        icon: Wrench,
        roles: ["ADMIN", "HR", "MANAGER"],
      },
      {
        label: "Close Project",
        href: "/projects/close-project",
        icon: FileCheck2,
        roles: ["ADMIN", "HR", "MANAGER"],
      },
      {
        label: "Invoice Submission",
        href: "/projects/invoice-submission",
        icon: Receipt,
        roles: ["ADMIN", "HR", "MANAGER"],
      },
      {
        label: "Invoice Tracking",
        href: "/projects/invoice-tracking",
        icon: HandCoins,
        roles: ["ADMIN", "HR", "MANAGER"],
      },
    ],
  },

  {
    group: "Finance",
    icon: CreditCard,
    roles: ["ADMIN", "HR"],
    items: [
      {
        label: "Payment Receipts",
        href: "/finance/payment-receipts",
        icon: Receipt,
        roles: ["ADMIN", "HR"],
      },
    ],
  },

  {
    group: "Vendors",
    icon: Store,
    roles: ["ADMIN", "HR", "MANAGER"],
    items: [
      {
        label: "Vendor Registration",
        href: "/vendors/vendor-registration",
        icon: Store,
        roles: ["ADMIN", "HR", "MANAGER"],
      },
      {
        label: "Purchase Order",
        href: "/vendors/purchase-order",
        icon: ShoppingCart,
        roles: ["ADMIN", "HR", "MANAGER"],
      },
      {
        label: "Vendor Payments",
        href: "/vendors/vendor-payments",
        icon: HandCoins,
        roles: ["ADMIN", "HR", "MANAGER"],
      },
    ],
  },

  {
    group: "Reports",
    icon: BarChart3,
    roles: ["ADMIN", "HR", "MANAGER"],
    items: [
      {
        label: "Attendance Reports",
        href: "/reports/attendance",
        icon: BarChart3,
        roles: ["ADMIN", "HR", "MANAGER"],
      },
    ],
  },
];
