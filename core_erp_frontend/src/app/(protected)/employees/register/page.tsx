"use client";

import { useEffect, useMemo, useState } from "react";
import API from "@/services/api";

type Gender = "Male" | "Female" | "Other";
type BloodGroup =
  | "A+"
  | "A-"
  | "B+"
  | "B-"
  | "O+"
  | "O-"
  | "AB+"
  | "AB-";

type Department = "Tech" | "Project Management" | "QA" | "Finance";

type Designation =
  | "VP"
  | "AVP"
  | "Site Supervisor"
  | "Project Manager"
  | "Sr. Project Manager"
  | "Sr. Project Executive";

type Status = "Active" | "Inactive" | "Terminated";

type FormState = {
  // personal
  first_name: string;
  middle_name: string;
  last_name: string;
  fathers_name: string;
  date_of_birth: string;
  gender: "" | Gender;
  blood_group: "" | BloodGroup;

  // employee
  employee_id: string;
  date_of_joining: string;
  work_location: string;
  department: "" | Department;
  designation: "" | Designation;
  is_manager: boolean;
  reporting_to: string;
  official_email: string;

  // contact
  mobile_number: string;
  personal_email: string;
  emergency_mobile: string;
  emergency_relation: string;

  // address
  current_address: string;
  current_state: string;
  current_city: string;
  permanent_address: string;
  permanent_state: string;
  permanent_city: string;

  // identity & bank
  aadhar_number: string;
  pan_number: string;
  bank_name: string;
  account_number: string;
  account_name: string;
  ifsc_code: string;
  pf_number: string;
  esi_number: string;

  // qualification
  highest_qualification: string;
  other_qualification: string;
  year_of_passing: string;
  total_experience: string;
  last_company: string;

  // salary
  salary_ctc: string;

  // status
  status: Status;
};

const initialState: FormState = {
  first_name: "",
  middle_name: "",
  last_name: "",
  fathers_name: "",
  date_of_birth: "",
  gender: "",
  blood_group: "",

  employee_id: "",
  date_of_joining: "",
  work_location: "",
  department: "",
  designation: "",
  is_manager: false,
  reporting_to: "",
  official_email: "",

  mobile_number: "",
  personal_email: "",
  emergency_mobile: "",
  emergency_relation: "",

  current_address: "",
  current_state: "",
  current_city: "",
  permanent_address: "",
  permanent_state: "",
  permanent_city: "",

  aadhar_number: "",
  pan_number: "",
  bank_name: "",
  account_number: "",
  account_name: "",
  ifsc_code: "",
  pf_number: "",
  esi_number: "",

  highest_qualification: "",
  other_qualification: "",
  year_of_passing: "",
  total_experience: "",
  last_company: "",

  salary_ctc: "",

  status: "Active",
};

function isValidEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export default function EmployeeRegisterPage() {
  const [form, setForm] = useState<FormState>(initialState);
  const [submitting, setSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  // Optional: restrict based on role from /auth/me
  const [role, setRole] = useState<string>("");

  useEffect(() => {
    (async () => {
      try {
        const res = await API.get("/auth/me");
        setRole(res.data?.role || "");
      } catch {
        setRole("");
      }
    })();
  }, []);

  const allowed = role === "ADMIN" || role === "HR" || role === "";
  // NOTE: role=="" means we didn't fetch role; don't block UI.

  const errors = useMemo(() => {
    const e: Record<string, string> = {};

    // Required
    if (!form.first_name.trim()) e.first_name = "First name is required";
    if (!form.last_name.trim()) e.last_name = "Last name is required";
    if (!form.employee_id.trim()) e.employee_id = "Employee ID is required";
    if (!form.date_of_joining) e.date_of_joining = "Date of joining is required";

    // Official email required + must be company
    if (!form.official_email.trim()) {
      e.official_email = "Official email is required";
    } else if (!isValidEmail(form.official_email)) {
      e.official_email = "Enter a valid email";
    } else if (!form.official_email.endsWith("@coresonant.com")) {
      e.official_email = "Must end with @coresonant.com";
    }

    // phone validations (backend expects 10 digits if provided)
    const phoneFields = ["mobile_number", "emergency_mobile"] as const;
    for (const f of phoneFields) {
      const val = form[f].trim();
      if (val && (!/^\d{10}$/.test(val))) {
        e[f] = "Must be 10 digits";
      }
    }

    // aadhar
    if (form.aadhar_number.trim() && !/^\d{12}$/.test(form.aadhar_number.trim())) {
      e.aadhar_number = "Aadhar must be 12 digits";
    }

    // PAN
    if (form.pan_number.trim() && form.pan_number.trim().length !== 10) {
      e.pan_number = "PAN must be 10 characters";
    }

    // total experience numeric
    if (form.total_experience.trim() && isNaN(Number(form.total_experience))) {
      e.total_experience = "Experience must be a number";
    }

    // salary numeric
    if (form.salary_ctc.trim() && isNaN(Number(form.salary_ctc))) {
      e.salary_ctc = "CTC must be a number";
    }

    // reporting_to must be number if provided
    if (form.reporting_to.trim() && isNaN(Number(form.reporting_to))) {
      e.reporting_to = "Reporting To must be a number (employee id)";
    }

    return e;
  }, [form]);

  const hasErrors = Object.keys(errors).length > 0;

  function setField<K extends keyof FormState>(key: K, value: FormState[K]) {
    setSuccessMsg("");
    setErrorMsg("");
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSuccessMsg("");
    setErrorMsg("");

    if (!allowed) {
      setErrorMsg("You do not have permission to register employees.");
      return;
    }

    if (hasErrors) {
      setErrorMsg("Fix the highlighted errors and try again.");
      return;
    }

    // Build payload for FastAPI
    const payload: any = {
      ...form,
      middle_name: form.middle_name || null,
      fathers_name: form.fathers_name || null,
      date_of_birth: form.date_of_birth || null,
      gender: form.gender || null,
      blood_group: form.blood_group || null,

      work_location: form.work_location || null,
      department: form.department || null,
      designation: form.designation || null,
      reporting_to: form.reporting_to ? Number(form.reporting_to) : null,

      mobile_number: form.mobile_number || null,
      personal_email: form.personal_email || null,
      emergency_mobile: form.emergency_mobile || null,
      emergency_relation: form.emergency_relation || null,

      current_address: form.current_address || null,
      current_state: form.current_state || null,
      current_city: form.current_city || null,
      permanent_address: form.permanent_address || null,
      permanent_state: form.permanent_state || null,
      permanent_city: form.permanent_city || null,

      aadhar_number: form.aadhar_number || null,
      pan_number: form.pan_number || null,
      bank_name: form.bank_name || null,
      account_number: form.account_number || null,
      account_name: form.account_name || null,
      ifsc_code: form.ifsc_code || null,
      pf_number: form.pf_number || null,
      esi_number: form.esi_number || null,

      highest_qualification: form.highest_qualification || null,
      other_qualification: form.other_qualification || null,
      year_of_passing: form.year_of_passing || null,
      total_experience: form.total_experience ? Number(form.total_experience) : null,
      last_company: form.last_company || null,

      salary_ctc: form.salary_ctc ? Number(form.salary_ctc) : null,

      // backend enum expects "Active"/"Inactive"/"Terminated"
      status: form.status,
      // defaults
      photograph_url: null,
      aadhar_file_url: null,
      resume_url: null,
      date_of_relieving: null,
    };

    try {
      setSubmitting(true);

      // IMPORTANT: your backend route is POST "/employees/"
      const res = await API.post("/employees/", payload);

      setSuccessMsg(
        `Employee created successfully (DB id: ${res.data?.id ?? "unknown"})`
      );
      setForm(initialState);
    } catch (err: any) {
      const detail =
        err?.response?.data?.detail ||
        err?.response?.data ||
        err?.message ||
        "Something went wrong";

      setErrorMsg(typeof detail === "string" ? detail : JSON.stringify(detail));
    } finally {
      setSubmitting(false);
    }
  }

  function Input({
    label,
    field,
    placeholder,
    type = "text",
  }: {
    label: string;
    field: keyof FormState;
    placeholder?: string;
    type?: string;
  }) {
    const value = form[field] as any;
    const error = errors[field as string];

    return (
      <div className="space-y-1">
        <label className="text-sm font-medium text-gray-800">{label}</label>
        <input
          type={type}
          value={value}
          placeholder={placeholder}
          onChange={(e) => setField(field as any, e.target.value as any)}
          className={`w-full rounded-2xl border px-3 py-2 text-sm outline-none transition ${
            error ? "border-red-500" : "border-gray-200"
          }`}
        />
        {error && <p className="text-xs text-red-600">{error}</p>}
      </div>
    );
  }

  function Select({
    label,
    field,
    options,
  }: {
    label: string;
    field: keyof FormState;
    options: string[];
  }) {
    const value = form[field] as any;
    const error = errors[field as string];

    return (
      <div className="space-y-1">
        <label className="text-sm font-medium text-gray-800">{label}</label>
        <select
          value={value}
          onChange={(e) => setField(field as any, e.target.value as any)}
          className={`w-full rounded-2xl border px-3 py-2 text-sm outline-none transition ${
            error ? "border-red-500" : "border-gray-200"
          }`}
        >
          <option value="">Select</option>
          {options.map((op) => (
            <option key={op} value={op}>
              {op}
            </option>
          ))}
        </select>
        {error && <p className="text-xs text-red-600">{error}</p>}
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="max-w-6xl">
        <h1 className="text-2xl font-bold text-gray-900">Employee Registration</h1>
        <p className="text-sm text-gray-600 mt-1">
          Fill the form and submit. Backend: <code>/employees/</code>
        </p>

        {!allowed && (
          <div className="mt-4 rounded-2xl border border-yellow-300 bg-yellow-50 px-4 py-3 text-sm text-yellow-800">
            You are logged in as <b>{role}</b>. You may not have access to register
            employees.
          </div>
        )}

        {errorMsg && (
          <div className="mt-4 rounded-2xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
            {errorMsg}
          </div>
        )}

        {successMsg && (
          <div className="mt-4 rounded-2xl border border-green-300 bg-green-50 px-4 py-3 text-sm text-green-700">
            {successMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="mt-6 space-y-8">
          {/* Personal */}
          <section className="rounded-3xl border bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">Personal Details</h2>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input label="First Name *" field="first_name" />
              <Input label="Middle Name" field="middle_name" />
              <Input label="Last Name *" field="last_name" />

              <Input label="Father's Name" field="fathers_name" />
              <Input label="Date of Birth" field="date_of_birth" type="date" />
              <Select
                label="Gender"
                field="gender"
                options={["Male", "Female", "Other"]}
              />

              <Select
                label="Blood Group"
                field="blood_group"
                options={["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]}
              />
            </div>
          </section>

          {/* Employee */}
          <section className="rounded-3xl border bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">Employee Details</h2>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input label="Employee ID *" field="employee_id" />
              <Input label="Date of Joining *" field="date_of_joining" type="date" />
              <Input label="Work Location" field="work_location" />

              <Select
                label="Department"
                field="department"
                options={["Tech", "Project Management", "QA", "Finance"]}
              />

              <Select
                label="Designation"
                field="designation"
                options={[
                  "VP",
                  "AVP",
                  "Site Supervisor",
                  "Project Manager",
                  "Sr. Project Manager",
                  "Sr. Project Executive",
                ]}
              />

              <div className="space-y-1">
                <label className="text-sm font-medium text-gray-800">
                  Is Manager?
                </label>
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={form.is_manager}
                    onChange={(e) => setField("is_manager", e.target.checked)}
                    className="h-4 w-4"
                  />
                  <span className="text-sm text-gray-700">
                    Mark if employee is a manager
                  </span>
                </div>
              </div>

              <Input
                label="Reporting To (Employee DB ID)"
                field="reporting_to"
                placeholder="Example: 12"
              />

              <Input
                label="Official Email *"
                field="official_email"
                placeholder="name@coresonant.com"
              />
            </div>
          </section>

          {/* Contact */}
          <section className="rounded-3xl border bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">Contact Details</h2>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input label="Mobile Number" field="mobile_number" />
              <Input label="Personal Email" field="personal_email" />
              <Input label="Emergency Mobile" field="emergency_mobile" />
              <Input label="Emergency Relation" field="emergency_relation" />
            </div>
          </section>

          {/* Address */}
          <section className="rounded-3xl border bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">Address</h2>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input label="Current Address" field="current_address" />
              <Input label="Current State" field="current_state" />
              <Input label="Current City" field="current_city" />

              <Input label="Permanent Address" field="permanent_address" />
              <Input label="Permanent State" field="permanent_state" />
              <Input label="Permanent City" field="permanent_city" />
            </div>
          </section>

          {/* Identity */}
          <section className="rounded-3xl border bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">
              Identity & Bank
            </h2>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input label="Aadhar Number" field="aadhar_number" />
              <Input label="PAN Number" field="pan_number" />
              <Input label="Bank Name" field="bank_name" />
              <Input label="Account Number" field="account_number" />
              <Input label="Account Name" field="account_name" />
              <Input label="IFSC Code" field="ifsc_code" />
              <Input label="PF Number" field="pf_number" />
              <Input label="ESI Number" field="esi_number" />
            </div>
          </section>

          {/* Qualification */}
          <section className="rounded-3xl border bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">
              Qualification & Experience
            </h2>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input label="Highest Qualification" field="highest_qualification" />
              <Input label="Other Qualification" field="other_qualification" />
              <Input label="Year of Passing" field="year_of_passing" type="date" />
              <Input label="Total Experience (years)" field="total_experience" />
              <Input label="Last Company" field="last_company" />
            </div>
          </section>

          {/* Salary + Status */}
          <section className="rounded-3xl border bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">
              Salary & Status
            </h2>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input label="Salary CTC" field="salary_ctc" />
              <Select
                label="Status"
                field="status"
                options={["Active", "Inactive", "Terminated"]}
              />
            </div>
          </section>

          {/* Submit */}
          <div className="flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={() => setForm(initialState)}
              className="rounded-2xl border px-4 py-2 text-sm hover:bg-gray-50"
              disabled={submitting}
            >
              Reset
            </button>

            <button
              type="submit"
              disabled={submitting || hasErrors}
              className={`rounded-2xl px-5 py-2 text-sm font-semibold text-white transition ${
                submitting || hasErrors
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-black hover:bg-gray-900"
              }`}
            >
              {submitting ? "Submitting..." : "Create Employee"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
