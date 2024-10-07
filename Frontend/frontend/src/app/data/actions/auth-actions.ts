"use server";

import { z } from "zod";

const schemaRegister = z.object({
  fullnames: z.string().min(3, {message: 'Full names must be at least 3 characters'}),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, {message: 'Password must be at least 8 characters'}),
  confirmPassword: z.string().min(8, {message: 'Password must be at least 8 characters'})
}).refine((data) => data.password === data.confirmPassword, {
  path: ['confirmPassword'],
  message: 'Passwords does not match'
})

// const schemaRegister = z.object({
//   fullname : z.string().min(4, {
//     message: "Full name must be between 4 and 50 characters",
//   }),
//   password: z.string().min(8, {
//     message: "Password must be between 8 and 100 characters",
//   }),
//   confirmPassword: z.string().min(8, {
//     message: "Password must be between 8 and 100 characters",
//   }),
//   email: z.string().email({
//     message: "Please enter a valid email address",
//   })
//   .refine((data) => data.password === data.confirmPassword, {
//     path: ['confirmPassword'],
//     message: 'Passwords does not match'
//   })
// })
export async function registerUserAction(prevState: any, formData: FormData) {
  console.log("Hello From Register User Action");

  const validateFields = schemaRegister.safeParse({
    fullnames: formData.get('fullnames'),
    password: formData.get("password"),
    confirmPassword: formData.get("confirmPassword"),
    email : formData.get("email"),
  });

  if(!validateFields.success){
    return {
      ...prevState,
      zodErrors: validateFields.error.flatten().fieldErrors,
      message: "Missing Fields. Failed to Register.",
    };
  };

  return {
    ...prevState,
    data: "ok",
  };
}