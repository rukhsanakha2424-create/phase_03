"use client";

/**
 * Task List Page
 * Main dashboard showing user's tasks
 */

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Plus, CheckCircle2, Circle } from "lucide-react";
import { useAuth } from "@/lib/auth/useAuth";
import { useTasks } from "@/lib/hooks/useTasks";
import { Button } from "@/components/common/Button";
import { TaskList } from "@/components/tasks/TaskList";
import { EmptyState } from "@/components/tasks/EmptyState";
import { ErrorAlert } from "@/components/common/ErrorAlert";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";

export default function TasksPage() {
  const router = useRouter();
  const { user, isAuthenticated } = useAuth();
  const {
    tasks,
    isLoading,
    error,
    fetchTasks,
    deleteTask,
    completeTask,
    incompleteTask,
    clearError,
  } = useTasks();
  const [isInitialized, setIsInitialized] = useState(false);

  // Fetch tasks on component mount
  useEffect(() => {
    if (!isAuthenticated || !user?.id) {
      return;
    }

    const loadTasks = async () => {
      try {
        await fetchTasks();
      } catch {
        // Error is handled by the hook
      } finally {
        setIsInitialized(true);
      }
    };

    loadTasks();
  }, [isAuthenticated, user?.id, fetchTasks]);

  // Show loading state while initializing
  if (!isInitialized && isLoading) {
    return <LoadingSpinner message="Loading your tasks..." />;
  }

  // Handle unauthenticated access
  if (!isAuthenticated || !user?.id) {
    return null; // Middleware should redirect to signin
  }

  const handleEdit = (taskId: string) => {
    router.push(`/tasks/${taskId}`);
  };

  const handleDelete = async (taskId: string) => {
    try {
      await deleteTask(taskId);
    } catch {
      // Error is handled by the hook
    }
  };

  const handleComplete = async (taskId: string) => {
    try {
      // Find the task to check its current state
      const task = tasks.find((t) => t.id === taskId);
      if (task?.completed) {
        // If already completed, mark as incomplete
        await incompleteTask(taskId);
      } else {
        // If not completed, mark as complete
        await completeTask(taskId);
      }
    } catch {
      // Error is handled by the hook
    }
  };

  const handleCreateClick = () => {
    router.push("/tasks/new");
  };

  // Calculate statistics
  const completedCount = tasks.filter((t) => t.completed).length;
  const incompleteCount = tasks.filter((t) => !t.completed).length;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h1
            className="text-4xl font-bold"
            style={{
              color: "#343a40",
              fontFamily: "'Space Grotesk', sans-serif",
            }}
          >
            Organify
          </h1>
          <p className="mt-2 text-slate-light">Organize and track your work</p>
        </div>
        <Button
          onClick={handleCreateClick}
          disabled={isLoading}
          variant="secondary"
          className="flex items-center  whitespace-nowrap"
        >
          <Plus size={18} />
          Create Task
        </Button>
      </div>

      {/* Statistics */}
      {tasks.length > 0 && (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-3">
          <div className="rounded-lg border border-organify-primary-light bg-neutral-light p-4">
            <div className="flex items-center gap-2">
              <Circle size={20} className="text-slate-light" />
              <div>
                <p className="text-sm text-slate-light">Active</p>
                <p className="text-2xl font-bold text-slate">
                  {incompleteCount}
                </p>
              </div>
            </div>
          </div>
          <div className="rounded-lg border border-organify-primary-light bg-neutral-light p-4">
            <div className="flex items-center gap-2">
              <CheckCircle2 size={20} className="text-success" />
              <div>
                <p className="text-sm text-slate-light">Completed</p>
                <p className="text-2xl font-bold text-slate">
                  {completedCount}
                </p>
              </div>
            </div>
          </div>
          {tasks.length > 0 && (
            <div className="rounded-lg border border-organify-primary-light bg-neutral-light p-4">
              <div>
                <p className="text-sm text-slate-light">Progress</p>
                <p className="text-2xl font-bold text-slate">
                  {Math.round((completedCount / tasks.length) * 100)}%
                </p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Error Alert */}
      {error && (
        <ErrorAlert
          message={error}
          title="Failed to load tasks"
          onDismiss={clearError}
        />
      )}

      {/* Task List */}
      {tasks.length > 0 ? (
        <TaskList
          tasks={tasks}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onComplete={handleComplete}
          isLoading={isLoading}
        />
      ) : (
        <EmptyState onCreateClick={handleCreateClick} />
      )}
    </div>
  );
}
