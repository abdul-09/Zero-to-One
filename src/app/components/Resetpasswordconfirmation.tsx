import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { AuthActions } from "@/app/auth/utils";
import { useSearchParams, useRouter } from "next/navigation";
type FormData = {
  password: string;
};

const ResetPasswordConfirmation = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>();
  const router = useRouter();
  const { resetPasswordConfirm } = AuthActions();

  const searchParams = useSearchParams();

  // State for UID and Token
  const [uid, setUid] = useState("");
  const [token, setToken] = useState("");

  // Extract UID and Token from URL
  useEffect(() => {
    const extractedUid = searchParams.get("uid");
    let extractedToken = searchParams.get("token");
    console.log("Extracted UID:", extractedUid);
    console.log("Extracted Token:", extractedToken);
    if (extractedToken && extractedToken.endsWith("/")) {
      extractedToken = extractedToken.slice(0, -1); 
    }

    if (extractedUid && extractedToken) {
      setUid(extractedUid as string);
      setToken(extractedToken as string);
    }
  }, [searchParams]);

  const onSubmit = async (data: FormData) => {
    console.log("Submitting data:", { uid, token, new_password: data.password, re_new_password: data.password });
    try {
      
      await resetPasswordConfirm(
        uid,
        token,
        data.password,
        data.password,
      ).res();
      alert("Password has been reset successfully.");
      router.push("/");
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (err) {
      console.log(err)
      alert("Failed to reset password. Please try again.");
    }
  };
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="px-8 py-6 mt-4 text-left bg-white shadow-lg w-1/3">
        <h3 className="text-2xl font-semibold">Set New Password</h3>
        <form onSubmit={handleSubmit(onSubmit)} className="mt-4">
          <label className="block" htmlFor="password">
            New Password
          </label>
          <input
            type="password"
            placeholder="Enter your new password"
            {...register("password", { required: true })}
            className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"
          />
          {errors.password && (
            <span className="text-xs text-red-600">Password is required</span>
          )}
          <div className="flex items-center justify-between mt-4">
            <button className="px-12 py-2 leading-5 text-white transition-colors duration-200 transform bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:bg-blue-700">
              Reset Password
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ResetPasswordConfirmation;
