"use client";

/**
 * TaskItem Component
 * Single task display with actions
 */

import React, { useState } from "react";
import { Trash2, Pencil, X, Check } from "lucide-react";
import { Task } from "@/lib/api/types";
import { formatRelativeTime } from "@/utils/formatting";
import { Button } from "@/components/common/Button";
import { PriorityBadge } from "@/components/common/PriorityBadge";
import { AnimatedCheckbox } from "@/components/common/AnimatedCheckbox";

interface TaskItemProps {
  task: Task;
  onEdit?: (taskId: string) => void;
  onDelete?: (taskId: string) => Promise<void>;
  onComplete?: (taskId: string) => Promise<void>;
  isLoading?: boolean;
}

export function TaskItem({
  task,
  onEdit,
  onDelete,
  onComplete,
  isLoading = false,
}: TaskItemProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isCompleting, setIsCompleting] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleDelete = async () => {
    if (!onDelete) return;

    setIsDeleting(true);
    try {
      await onDelete(task.id);
      setShowDeleteConfirm(false);
    } catch {
      // Error is handled by parent
    } finally {
      setIsDeleting(false);
    }
  };

  const handleComplete = async () => {
    if (!onComplete) return;

    setIsCompleting(true);
    try {
      await onComplete(task.id);
    } catch {
      // Error is handled by parent
    } finally {
      setIsCompleting(false);
    }
  };

  return (
    <div
      className={`group relative rounded-xl border transition-all duration-200 ${
        task.completed
          ? "border-slate-light bg-neutral-dark hover:bg-neutral"
          : "border-slate-light bg-neutral-light hover:border-slate hover:shadow-md"
      }`}
    >
      <div className="flex items-start gap-4 p-4">
        {/* Completion Checkbox */}
        <div className="flex-shrink-0 pt-1">
          <AnimatedCheckbox
            id={`task-${task.id}`}
            checked={task.completed}
            onChange={handleComplete}
            disabled={isCompleting || isLoading}
            ariaLabel="Mark task complete"
          />
        </div>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap items-start gap-2 sm:items-center">
            <h3
              className={`text-base font-semibold transition-colors ${
                task.completed ? "text-slate-light line-through" : "text-slate"
              }`}
            >
              {task.title}
            </h3>
            {task.priority && (
              <PriorityBadge
                priority={task.priority}
                size="sm"
                showText={true}
              />
            )}
          </div>

          {task.notes && (
            <p
              className={`mt-2 text-sm leading-relaxed transition-colors ${
                task.completed ? "text-slate-light" : "text-slate-light"
              }`}
            >
              {task.notes}
            </p>
          )}

          <p className="mt-3 text-xs text-slate-light">
            Created {formatRelativeTime(task.createdAt)}
          </p>
        </div>

        {/* Actions */}
        <div className="flex-shrink-0 flex gap-1 opacity-0 transition-opacity duration-200 group-hover:opacity-100 sm:opacity-100">
          {onEdit && (
            <button
              onClick={() => onEdit(task.id)}
              disabled={isLoading || isDeleting}
              className="rounded-lg p-2 text-slate-light hover:bg-organify-primary/10 hover:text-organify-primary transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              title="Edit task"
              aria-label="Edit task"
            >
              <Pencil size={18} strokeWidth={2} />
            </button>
          )}

          {onDelete && (
            <>
              {showDeleteConfirm ? (
                <div className="absolute right-4 top-16 z-20 flex gap-1 rounded-lg border border-error/20 bg-neutral-light p-2 shadow-lg">
                  <button
                    onClick={handleDelete}
                    disabled={isDeleting}
                    className="flex items-center gap-1 rounded px-2 py-1 text-sm font-medium text-error hover:bg-error/10 transition-colors disabled:opacity-50"
                    title="Confirm delete"
                  >
                    <Check size={16} />
                    Delete
                  </button>
                  <button
                    onClick={() => setShowDeleteConfirm(false)}
                    className="flex items-center gap-1 rounded px-2 py-1 text-sm text-slate-light hover:bg-slate/10 transition-colors"
                    title="Cancel delete"
                  >
                    <X size={16} />
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setShowDeleteConfirm(true)}
                  disabled={isLoading || isDeleting}
                  className="rounded-lg p-2 text-slate-light hover:bg-error/10 hover:text-error transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  title="Delete task"
                  aria-label="Delete task"
                >
                  <Trash2 size={18} strokeWidth={2} />
                </button>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
