import React, { useEffect, useRef } from "react";

const DynamicBackground = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    let animationFrameId;
    let mouseX = 0;
    let mouseY = 0;
    
    // Track mouse position
    const handleMouseMove = (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    };
    
    window.addEventListener('mousemove', handleMouseMove);
    
    // Handle resize
    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    
    window.addEventListener('resize', handleResize);
    handleResize();
    
    // Create stars (small static points)
    const stars = [];
    const starCount = Math.floor(canvas.width * canvas.height / 12000);
    
    for (let i = 0; i < starCount; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 1.5,
        opacity: Math.random() * 0.8 + 0.2,
        twinkleSpeed: Math.random() * 0.03
      });
    }
    
    // Create nodes (larger interactive points)
    const nodes = [];
    const nodeCount = Math.floor(canvas.width * canvas.height / 30000);
    
    for (let i = 0; i < nodeCount; i++) {
      nodes.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 3 + 1,
        vx: Math.random() * 0.4 - 0.2,
        vy: Math.random() * 0.4 - 0.2,
        color: Math.random() > 0.7 ? 'rgba(6, 182, 212, alpha)' : 'rgba(20, 184, 166, alpha)', // cyan or teal
        pulseFactor: 0,
        pulseSpeed: Math.random() * 0.03 + 0.01,
        connections: []
      });
    }
    
    // Time tracking
    let time = 0;
    
    // Create 3-5 ambient light sources
    const ambientLights = [];
    const lightCount = Math.floor(Math.random() * 3) + 3;
    
    for (let i = 0; i < lightCount; i++) {
      ambientLights.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 300 + 200,
        opacity: Math.random() * 0.15 + 0.05,
        vx: Math.random() * 0.5 - 0.25,
        vy: Math.random() * 0.5 - 0.25,
        color: Math.random() > 0.5 ? 
          'rgba(6, 182, 212, alpha)' : // cyan
          'rgba(20, 184, 166, alpha)' // teal
      });
    }
    
    // Animation loop
    const animate = () => {
      // Semi-transparent background to create trail effect
      ctx.fillStyle = 'rgba(15, 23, 42, 0.3)'; // slate-950 with low opacity
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      time += 0.005;
      
      // Update and render ambient lights
      ambientLights.forEach(light => {
        // Move lights very slowly
        light.x += light.vx;
        light.y += light.vy;
        
        // Bounce off edges
        if (light.x < 0 || light.x > canvas.width) light.vx *= -1;
        if (light.y < 0 || light.y > canvas.height) light.vy *= -1;
        
        // Draw gradient light
        const gradient = ctx.createRadialGradient(
          light.x, light.y, 0,
          light.x, light.y, light.radius
        );
        
        gradient.addColorStop(0, light.color.replace('alpha', light.opacity * 0.8));
        gradient.addColorStop(0.5, light.color.replace('alpha', light.opacity * 0.3));
        gradient.addColorStop(1, light.color.replace('alpha', 0));
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(light.x, light.y, light.radius, 0, Math.PI * 2);
        ctx.fill();
      });
      
      // Render stars with twinkling effect
      stars.forEach(star => {
        const twinkle = Math.sin(time * star.twinkleSpeed * 10) * 0.5 + 0.5;
        ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity * twinkle})`;
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fill();
      });
      
      // Calculate node connections
      nodes.forEach(node => {
        node.connections = [];
      });
      
      // Find connections between nodes (relatively close nodes)
      const connectionDistance = canvas.width * 0.1;
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[i].x - nodes[j].x;
          const dy = nodes[i].y - nodes[j].y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance < connectionDistance) {
            nodes[i].connections.push({ node: nodes[j], distance });
            nodes[j].connections.push({ node: nodes[i], distance });
          }
        }
      }
      
      // Update and render nodes
      nodes.forEach(node => {
        // Move nodes
        node.x += node.vx;
        node.y += node.vy;
        
        // Bounce off edges with a bit of randomness
        if (node.x < 0 || node.x > canvas.width) {
          node.vx *= -1;
          node.vx += (Math.random() - 0.5) * 0.1;
        }
        if (node.y < 0 || node.y > canvas.height) {
          node.vy *= -1;
          node.vy += (Math.random() - 0.5) * 0.1;
        }
        
        // Add some random movement
        if (Math.random() < 0.01) {
          node.vx += (Math.random() - 0.5) * 0.1;
          node.vy += (Math.random() - 0.5) * 0.1;
          
          // Keep speed in check
          const speed = Math.sqrt(node.vx * node.vx + node.vy * node.vy);
          if (speed > 0.5) {
            node.vx = (node.vx / speed) * 0.5;
            node.vy = (node.vy / speed) * 0.5;
          }
        }
        
        // Update pulse animation
        node.pulseFactor += node.pulseSpeed;
        if (node.pulseFactor > 1) {
          node.pulseFactor = 0;
        }
        
        // Draw connections first (so they appear behind nodes)
        node.connections.forEach(connection => {
          const opacity = 1 - (connection.distance / connectionDistance);
          ctx.strokeStyle = node.color.replace('alpha', opacity * 0.2);
          ctx.lineWidth = 0.5;
          ctx.beginPath();
          ctx.moveTo(node.x, node.y);
          ctx.lineTo(connection.node.x, connection.node.y);
          ctx.stroke();
        });
        
        // Calculate distance to mouse for interactive effect
        const dx = mouseX - node.x;
        const dy = mouseY - node.y;
        const distanceToMouse = Math.sqrt(dx * dx + dy * dy);
        const mouseInfluence = Math.max(0, 1 - (distanceToMouse / 200));
        
        // Draw node with pulsing effect + mouse influence
        const pulse = Math.sin(node.pulseFactor * Math.PI) * 0.5 + 0.5;
        const radius = node.radius * (1 + pulse * 0.5 + mouseInfluence * 2);
        const opacity = 0.6 + pulse * 0.4 + mouseInfluence * 0.4;
        
        ctx.fillStyle = node.color.replace('alpha', opacity);
        ctx.beginPath();
        ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
        ctx.fill();
        
        // Add glow effect for larger nodes or when near mouse
        if (node.radius > 2 || mouseInfluence > 0.5) {
          const glowRadius = radius * (1.5 + mouseInfluence);
          const gradient = ctx.createRadialGradient(
            node.x, node.y, radius * 0.5,
            node.x, node.y, glowRadius
          );
          
          gradient.addColorStop(0, node.color.replace('alpha', opacity * 0.8));
          gradient.addColorStop(1, node.color.replace('alpha', 0));
          
          ctx.fillStyle = gradient;
          ctx.beginPath();
          ctx.arc(node.x, node.y, glowRadius, 0, Math.PI * 2);
          ctx.fill();
        }
      });
      
      // Create occasional energy pulse from center (randomly)
      if (Math.random() < 0.002) {
        const pulseX = Math.random() * canvas.width;
        const pulseY = Math.random() * canvas.height;
        
        for (let radius = 0; radius < 100; radius += 5) {
          setTimeout(() => {
            ctx.strokeStyle = `rgba(6, 182, 212, ${(100 - radius) / 100 * 0.4})`;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(pulseX, pulseY, radius, 0, Math.PI * 2);
            ctx.stroke();
          }, radius * 20);
        }
      }
      
      animationFrameId = requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);
  
  return <canvas ref={canvasRef} className="fixed inset-0 -z-10" />;
};

export default DynamicBackground;