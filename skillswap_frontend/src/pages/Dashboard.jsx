import { useAuthStore } from "../store/authStore";
import NavBar from '../components/NavBar';
import { useEffect } from "react";

export default function Dashboard() {
    const { user, fetchUserSkills } = useAuthStore();

    useEffect(() => {
        fetchUserSkills();
    }, []);

    if (!user) {
        return <div className="p-4 text-red-500">Not logged in.</div>;
    }

    return (
        <div>
            <NavBar />
            <div className="pt-24 px-4 max-w-5xl mx-auto">
                <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

                <div className="space-y-4 text-lg">
                    <p><span className="font-semibold">Name:</span> {user.full_name}</p>
                    <p><span className="font-semibold">Email:</span> {user.email}</p>
                </div>

                <div className="mt-6">
                    <h2 className="text-xl font-semibold mb-3">Skills you can teach</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                        {user.skills_teach?.length ? (
                            user.skills_teach.map((skill, idx) => (
                                <div key={idx} className="bg-purple-100 text-purple-800 p-3 rounded shadow">
                                    {skill}
                                </div>
                            ))
                        ) : (
                            <p>No skills added yet.</p>
                        )}
                    </div>
                </div>

                <div className="mt-6">
                    <h2 className="text-xl font-semibold mb-3">Skills you would like to learn</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                        {user.skills_learn?.length ? (
                            user.skills_learn.map((skill, idx) => (
                                <div key={idx} className="bg-blue-100 text-blue-800 p-3 rounded shadow">
                                    {skill}
                                </div>
                            ))
                        ) : (
                            <p>No skills added yet.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
