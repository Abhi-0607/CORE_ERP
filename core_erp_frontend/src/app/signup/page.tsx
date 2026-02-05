"use client";

import API from "@/services/api";
import { use } from "react";
import { useForm } from "react-hook-form";

type FormData = {
  full_name: string;
  email: string;
  password: string;
  confirm_password: string;
  role: string;
};

export default function Signup() {
  const { register, handleSubmit } = useForm<FormData>();

  const onSubmit = async (data: FormData) => {
    try {
      await API.post("/auth/signup", data);
      alert("Signup Successful!");
    } catch (err: any) {
      alert(err.response?.data?.detail || "Error signing up");
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("full_name")} placeholder="Full Name" />
      <input {...register("email")} placeholder="Email" type="email" />
      <input {...register("password")} placeholder="Password" type="password" />
      <input {...register("confirm_password")} placeholder="Confirm Password" type="password" />
      <select {...register("role")}>
        <option value="ADMIN">Admin</option>
        <option value="HR">HR</option>
      </select>
      <button type="submit">Signup</button>
    </form>
  );
}
