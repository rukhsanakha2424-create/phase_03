/**
 * Features Component
 * Two-part features section:
 * 1. Dark section highlighting pain points with modern card design
 * 2. Value proposition cards (3-column layout)
 * Inspired by professional SaaS landing pages
 * Part of User Story 1: Landing Page
 */

interface PainPoint {
  icon: React.ReactNode;
  title: string;
  description: string;
}

interface ValueProposition {
  icon: React.ReactNode;
  number: string;
  title: string;
  description: string;
}

interface FeaturesProps {
  painPoints?: PainPoint[];
  valueProps?: ValueProposition[];
}

// SVG Icons
const AlertIcon = () => (
  <svg
    className="w-6 h-6"
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
    />
  </svg>
);

const CheckCircleIcon = () => (
  <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
    <path
      fillRule="evenodd"
      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
      clipRule="evenodd"
    />
  </svg>
);

const BoltIcon = () => (
  <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
    <path
      fillRule="evenodd"
      d="M11.3 1.046A1 1 0 0110 2v5H6a1 1 0 00-.82 1.573l6.92 8.4a1 1 0 001.82-.577V11h4a1 1 0 00.82-1.573l-6.92-8.4z"
      clipRule="evenodd"
    />
  </svg>
);

const LockIcon = () => (
  <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
    <path
      fillRule="evenodd"
      d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
      clipRule="evenodd"
    />
  </svg>
);

export function Features({
  valueProps = [
    {
      icon: <CheckCircleIcon />,
      number: "1",
      title: "Organify",
      description:
        "Instantly capture your thoughts and tasks with a clear, distraction-free interface.",
    },
    {
      icon: <BoltIcon />,
      number: "2",
      title: "Task Manager",
      description:
        "Our smart prioritization algorithm highlights the one thing that matters today.",
    },
    {
      icon: <LockIcon />,
      number: "3",
      title: "Tasks",
      description:
        "Experience the thrill of completion with every finished item and track progress in real time.",
    },
  ],
}: FeaturesProps) {
  return (
    <>
      {/* DARK SECTION: Why Traditional Planners Fail */}
      {/* // <section className="relative bg-gradient-to-br from-slate-dark via-slate to-slate-dark py-20 sm:py-32 px-4 sm:px-6 lg:px-8 overflow-hidden"> */}

      {/* LIGHT SECTION: The Promise of Simplicity */}
      <section className="relative bg-slate py-20 sm:py-32 px-4 sm:px-6 lg:px-8 overflow-hidden">
        {/* Subtle background elements */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-violet/3 rounded-full -mr-48 -mt-48 blur-3xl"></div>

        <div className="w-full max-w-6xl mx-auto relative z-10">
          {/* Section Header */}
          <div className="text-center max-w-3xl mx-auto mb-16 sm:mb-20">
            <h2
              className="text-4xl sm:text-5xl font-medium mb-6 tracking-tight text-white"
              style={{
                color: "#ffffff",
                fontFamily: "'Space Grotesk', sans-serif",
              }}
            >
              The Promise of Simplicity
            </h2>
            <p className="text-lg font-light leading-relaxed text-slate-300">
              Three steps to your most productive self
            </p>
          </div>

          {/* Value Proposition Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {valueProps.map((prop, index) => (
              <div key={index} className="group relative text-center">
                {/* Number badge */}
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-violet-light to-violet-dark text-white font-bold text-2xl mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                  {prop.number}
                </div>

                {/* Icon would go here if using React.ReactNode */}
                <h3
                  className="text-2xl font-light mb-4"
                  style={{
                    color: "#ffffff",
                    fontFamily: "'Space Grotesk', sans-serif",
                  }}
                >
                  {prop.title}
                </h3>

                <p className="text-slate-300 leading-relaxed">
                  {prop.description}
                </p>

                {/* Optional: bottom accent line */}
                <div className="absolute bottom-0 left-1/2 -translate-x-1/2 h-1 w-0 bg-gradient-to-r from-transparent via-violet to-transparent group-hover:w-full transition-all duration-500 rounded-full"></div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
