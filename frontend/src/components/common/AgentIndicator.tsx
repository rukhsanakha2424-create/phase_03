'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Bot, BotMessageSquare } from 'lucide-react';
import { apiClient } from '@/lib/api/client';

interface AgentStatus {
  status: string; // "online" or "offline"
}

export function AgentIndicator() {
  const [agentStatus, setAgentStatus] = useState<AgentStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAgentStatus = async () => {
      try {
        const data: AgentStatus = await apiClient.get('/api/v1/agent/status');
        setAgentStatus(data);
        setError(null); // Clear any previous errors
      } catch (err) {
        console.error('Error fetching agent status:', err);
        
        // Check if it's a network error
        if (err && typeof err === 'object' && 'code' in err && err.code === 'NETWORK_ERROR') {
          setError('AI agent service unavailable');
        } else {
          setError('Unable to connect to AI agent');
        }
        
        // Set a default offline status when API is unreachable
        setAgentStatus({ status: 'offline' });
      } finally {
        setLoading(false);
      }
    };

    fetchAgentStatus();

    // Poll for updates every 30 seconds
    const interval = setInterval(fetchAgentStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-blue-500/10 border border-blue-500/20">
        <motion.div
          className="w-3 h-3 rounded-full bg-blue-500"
          animate={{ scale: [1, 1.2, 1] }}
          transition={{ repeat: Infinity, duration: 1.5 }}
        />
        <span className="text-xs font-medium text-blue-500">AI Agent</span>
      </div>
    );
  }

  if (error && !agentStatus) {
    return (
      <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-red-500/10 border border-red-500/20">
        <div className="w-3 h-3 rounded-full bg-red-500" />
        <span className="text-xs font-medium text-red-500">AI Offline</span>
      </div>
    );
  }

  // Show as offline when there's an error but we have a default status
  if (error && agentStatus) {
    return (
      <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-yellow-500/10 border border-yellow-500/20">
        <div className="w-3 h-3 rounded-full bg-yellow-500" />
        <span className="text-xs font-medium text-yellow-500">AI Limited</span>
      </div>
    );
  }

  const isOnline = agentStatus.status === 'online';

  return (
    <div className="group relative">
      <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border cursor-pointer transition-all ${
        isOnline
          ? 'bg-green-500/10 border-green-500/20 hover:bg-green-500/20'
          : 'bg-yellow-500/10 border-yellow-500/20 hover:bg-yellow-500/20'
      }`}>
        <motion.div
          className="w-3 h-3 rounded-full"
          animate={{ scale: isOnline ? [1, 1.2, 1] : 1 }}
          transition={{ repeat: isOnline ? Infinity : 0, duration: 1.5 }}
          style={{ backgroundColor: isOnline ? '#10b981' : '#f59e0b' }}
        />
        <div className="flex items-center gap-1">
          <Bot size={14} className={isOnline ? "text-green-500" : "text-yellow-500"} />
          <span className={`text-xs font-medium ${
            isOnline ? "text-green-600" : "text-yellow-600"
          }`}>
            AI Agent
          </span>
        </div>
      </div>

      {/* Tooltip */}
      <div className="absolute left-1/2 transform -translate-x-1/2 bottom-full mb-2 hidden group-hover:block z-50">
        <div className="bg-slate-800 text-white text-xs rounded-lg py-2 px-3 whitespace-nowrap">
          <div className="font-medium">Taskie AI Agent</div>
          <div className="text-slate-300 mt-1">
            Status: <span className={isOnline ? "text-green-400" : "text-yellow-400"}>
              {isOnline ? "Online" : "Offline"}
            </span>
          </div>
          <div className="text-slate-400 text-[10px] mt-1">
            Last activity: Just now
          </div>
        </div>
        <div className="absolute left-1/2 transform -translate-x-1/2 translate-y-full w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-slate-800"></div>
      </div>
    </div>
  );
}