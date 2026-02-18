"use client";

import React, { useEffect, useMemo, useState } from "react";
import API from "@/services/api";
import { useRouter } from "next/navigation";

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

/* -----------------------------
   INPUT COMPONENT (OUTSIDE PAGE)
------------------------------ */
function Input({
  label,
  value,
  placeholder,
  type = "text",
  error,
  onChange,
}: {
  label: string;
  value: any;
  placeholder?: string;
  type?: string;
  error?: string;
  onChange: (val: string) => void;
}) {
  return (
    <div className="space-y-1">
      <label className="text-sm font-medium text-gray-800">{label}</label>
      <input
        type={type}
        value={value}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
        className={`w-full rounded-2xl border px-3 py-2 text-sm outline-none transition ${
          error ? "border-red-500" : "border-gray-200"
        }`}
      />
      {error && <p className="text-xs text-red-600">{error}</p>}
    </div>
  );
}

/* -----------------------------
   SELECT COMPONENT (OUTSIDE PAGE)
------------------------------ */
function Select({
  label,
  value,
  options,
  error,
  onChange,
}: {
  label: string;
  value: any;
  options: string[];
  error?: string;
  onChange: (val: string) => void;
}) {
  return (
    <div className="space-y-1">
      <label className="text-sm font-medium text-gray-800">{label}</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
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

export default function EmployeeRegisterPage() {
  const router = useRouter();

  const [form, setForm] = useState<FormState>(initialState);
  const [submitting, setSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

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

  const errors = useMemo(() => {
    const e: Record<string, string> = {};

    if (!form.first_name.trim()) e.first_name = "First name is required";
    if (!form.last_name.trim()) e.last_name = "Last name is required";
    if (!form.employee_id.trim()) e.employee_id = "Employee ID is required";
    if (!form.date_of_joining) e.date_of_joining = "Date of joining is required";

    if (!form.official_email.trim()) {
      e.official_email = "Official email is required";
    } else if (!isValidEmail(form.official_email)) {
      e.official_email = "Enter a valid email";
    } else if (!form.official_email.endsWith("@coresonant.com")) {
      e.official_email = "Must end with @coresonant.com";
    }

    const phoneFields = ["mobile_number", "emergency_mobile"] as const;
    for (const f of phoneFields) {
      const val = form[f].trim();
      if (val && !/^\d{10}$/.test(val)) {
        e[f] = "Must be 10 digits";
      }
    }

    if (form.aadhar_number.trim() && !/^\d{12}$/.test(form.aadhar_number.trim())) {
      e.aadhar_number = "Aadhar must be 12 digits";
    }

    if (form.pan_number.trim() && form.pan_number.trim().length !== 10) {
      e.pan_number = "PAN must be 10 characters";
    }

    if (form.total_experience.trim() && isNaN(Number(form.total_experience))) {
      e.total_experience = "Experience must be a number";
    }

    if (form.salary_ctc.trim() && isNaN(Number(form.salary_ctc))) {
      e.salary_ctc = "CTC must be a number";
    }

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

      status: form.status,
      photograph_url: null,
      aadhar_file_url: null,
      resume_url: null,
      date_of_relieving: null,
    };

    try {
      setSubmitting(true);

      const res = await API.post("/employees/", payload);

      setSuccessMsg(
        `Employee created successfully`
      );
      setForm(initialState);
      // Redirect after a short delay (so user sees success)
      setTimeout(() => {
        router.push("/employees/list");
      }, 800);
      
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

  return (
    <div className="p-6">
      <div className="max-w-6xl">
        <h1 className="text-2xl font-bold text-gray-900">Employee Registration</h1>

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
              <Input
                label="First Name *"
                value={form.first_name}
                error={errors.first_name}
                onChange={(v) => setField("first_name", v)}
              />

              <Input
                label="Middle Name"
                value={form.middle_name}
                error={errors.middle_name}
                onChange={(v) => setField("middle_name", v)}
              />

              <Input
                label="Last Name *"
                value={form.last_name}
                error={errors.last_name}
                onChange={(v) => setField("last_name", v)}
              />

              <Input
                label="Father's Name"
                value={form.fathers_name}
                error={errors.fathers_name}
                onChange={(v) => setField("fathers_name", v)}
              />

              <Input
                label="Date of Birth"
                type="date"
                value={form.date_of_birth}
                error={errors.date_of_birth}
                onChange={(v) => setField("date_of_birth", v)}
              />

              <Select
                label="Gender"
                value={form.gender}
                error={errors.gender}
                options={["Male", "Female", "Other"]}
                onChange={(v) => setField("gender", v as any)}
              />

              <Select
                label="Blood Group"
                value={form.blood_group}
                error={errors.blood_group}
                options={["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]}
                onChange={(v) => setField("blood_group", v as any)}
              />
            </div>
          </section>

          {/* Employee */}
          <section className="rounded-3xl border bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">Employee Details</h2>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input
                label="Employee ID *"
                value={form.employee_id}
                error={errors.employee_id}
                onChange={(v) => setField("employee_id", v)}
              />

              <Input
                label="Date of Joining *"
                type="date"
                value={form.date_of_joining}
                error={errors.date_of_joining}
                onChange={(v) => setField("date_of_joining", v)}
              />

              <Input
                label="Work Location"
                value={form.work_location}
                error={errors.work_location}
                onChange={(v) => setField("work_location", v)}
              />

              <Select
                label="Department"
                value={form.department}
                error={errors.department}
                options={["Tech", "Project Management", "QA", "Finance"]}
                onChange={(v) => setField("department", v as any)}
              />

              <Select
                label="Designation"
                value={form.designation}
                error={errors.designation}
                options={[
                  "VP",
                  "AVP",
                  "Site Supervisor",
                  "Project Manager",
                  "Sr. Project Manager",
                  "Sr. Project Executive",
                ]}
                onChange={(v) => setField("designation", v as any)}
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
                value={form.reporting_to}
                error={errors.reporting_to}
                placeholder="Example: 12"
                onChange={(v) => setField("reporting_to", v)}
              />

              <Input
                label="Official Email *"
                value={form.official_email}
                error={errors.official_email}
                placeholder="name@coresonant.com"
                onChange={(v) => setField("official_email", v)}
              />
            </div>
          </section>

          {/* Contact */}
          <section className="rounded-3xl border bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">Contact Details</h2>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input
                label="Mobile Number"
                value={form.mobile_number}
                error={errors.mobile_number}
                onChange={(v) => setField("mobile_number", v)}
              />

              <Input
                label="Personal Email"
                value={form.personal_email}
                error={errors.personal_email}
                onChange={(v) => setField("personal_email", v)}
              />

              <Input
                label="Emergency Mobile"
                value={form.emergency_mobile}
                error={errors.emergency_mobile}
                onChange={(v) => setField("emergency_mobile", v)}
              />

              <Input
                label="Emergency Relation"
                value={form.emergency_relation}
                error={errors.emergency_relation}
                onChange={(v) => setField("emergency_relation", v)}
              />
            </div>
          </section>

          {/* Address */}
          <section className="rounded-3xl border bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">Address</h2>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input
                label="Current Address"
                value={form.current_address}
                error={errors.current_address}
                onChange={(v) => setField("current_address", v)}
              />

              <Input
                label="Current State"
                value={form.current_state}
                error={errors.current_state}
                onChange={(v) => setField("current_state", v)}
              />

              <Input
                label="Current City"
                value={form.current_city}
                error={errors.current_city}
                onChange={(v) => setField("current_city", v)}
              />

              <Input
                label="Permanent Address"
                value={form.permanent_address}
                error={errors.permanent_address}
                onChange={(v) => setField("permanent_address", v)}
              />

              <Input
                label="Permanent State"
                value={form.permanent_state}
                error={errors.permanent_state}
                onChange={(v) => setField("permanent_state", v)}
              />

              <Input
                label="Permanent City"
                value={form.permanent_city}
                error={errors.permanent_city}
                onChange={(v) => setField("permanent_city", v)}
              />
            </div>
          </section>

          {/* Identity */}
          <section className="rounded-3xl border bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">
              Identity & Bank
            </h2>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input
                label="Aadhar Number"
                value={form.aadhar_number}
                error={errors.aadhar_number}
                onChange={(v) => setField("aadhar_number", v)}
              />

              <Input
                label="PAN Number"
                value={form.pan_number}
                error={errors.pan_number}
                onChange={(v) => setField("pan_number", v)}
              />

              <Input
                label="Bank Name"
                value={form.bank_name}
                error={errors.bank_name}
                onChange={(v) => setField("bank_name", v)}
              />

              <Input
                label="Account Number"
                value={form.account_number}
                error={errors.account_number}
                onChange={(v) => setField("account_number", v)}
              />

              <Input
                label="Account Name"
                value={form.account_name}
                error={errors.account_name}
                onChange={(v) => setField("account_name", v)}
              />

              <Input
                label="IFSC Code"
                value={form.ifsc_code}
                error={errors.ifsc_code}
                onChange={(v) => setField("ifsc_code", v)}
              />

              <Input
                label="PF Number"
                value={form.pf_number}
                error={errors.pf_number}
                onChange={(v) => setField("pf_number", v)}
              />

              <Input
                label="ESI Number"
                value={form.esi_number}
                error={errors.esi_number}
                onChange={(v) => setField("esi_number", v)}
              />
            </div>
          </section>

          {/* Qualification */}
          <section className="rounded-3xl border bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">
              Qualification & Experience
            </h2>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input
                label="Highest Qualification"
                value={form.highest_qualification}
                error={errors.highest_qualification}
                onChange={(v) => setField("highest_qualification", v)}
              />

              <Input
                label="Other Qualification"
                value={form.other_qualification}
                error={errors.other_qualification}
                onChange={(v) => setField("other_qualification", v)}
              />

              <Input
                label="Year of Passing"
                type="date"
                value={form.year_of_passing}
                error={errors.year_of_passing}
                onChange={(v) => setField("year_of_passing", v)}
              />

              <Input
                label="Total Experience (years)"
                value={form.total_experience}
                error={errors.total_experience}
                onChange={(v) => setField("total_experience", v)}
              />

              <Input
                label="Last Company"
                value={form.last_company}
                error={errors.last_company}
                onChange={(v) => setField("last_company", v)}
              />
            </div>
          </section>

          {/* Salary + Status */}
          <section className="rounded-3xl border bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">
              Salary & Status
            </h2>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input
                label="Salary CTC"
                value={form.salary_ctc}
                error={errors.salary_ctc}
                onChange={(v) => setField("salary_ctc", v)}
              />

              <Select
                label="Status"
                value={form.status}
                error={errors.status}
                options={["Active", "Inactive", "Terminated"]}
                onChange={(v) => setField("status", v as any)}
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
