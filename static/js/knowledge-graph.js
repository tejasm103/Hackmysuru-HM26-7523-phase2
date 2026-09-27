/**
 * AdaptiveLearn AI - Knowledge Graph Visualizer
 * Renders the prerequisite DAG using dynamic SVG/Canvas with color-coded node states:
 * GREEN (Mastered >= 70%), BLUE (Learning), YELLOW (Needs Practice), RED (Struggling), LOCK (Locked).
 */

class KnowledgeGraphVisualizer {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.options = options;
    this.data = null;
  }

  async load(courseId = 1) {
    if (!this.container) return;
    this.container.innerHTML = `<div style="text-align:center; padding:40px; color:#94a3b8;">Loading Knowledge Graph...</div>`;
    try {
      this.data = await API.getKnowledgeGraph(courseId);
      this.render();
    } catch (err) {
      this.container.innerHTML = `<div style="color:#ef4444; padding:20px;">Failed to render Knowledge Graph: ${err.message}</div>`;
    }
  }

  render() {
    if (!this.data || !this.data.nodes) return;
    const { nodes, edges } = this.data;
    
    const width = this.container.clientWidth || 900;
    const height = 480;
    const nodeRadius = 38;

    // Layout nodes horizontally based on sequence_order
    const totalNodes = nodes.length;
    const spacingX = Math.max(140, (width - 120) / Math.max(1, totalNodes - 1));
    
    const nodePositions = {};
    nodes.forEach((node, i) => {
      // Alternate Y coordinates slightly for dynamic aesthetic curve
      const yOffset = (i % 2 === 0) ? height * 0.42 : height * 0.58;
      nodePositions[node.id] = {
        x: 70 + (i * spacingX),
        y: yOffset,
        node: node
      };
    });

    // Generate SVG
    let svgHtml = `
      <svg width="100%" height="${height}" viewBox="0 0 ${Math.max(width, 70 + totalNodes * spacingX)} ${height}" 
           style="background: rgba(6, 10, 24, 0.6); border-radius: 16px; border: 1px solid rgba(255,255,255,0.06); overflow: visible;">
        <defs>
          <linearGradient id="edgeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#6366f1" stop-opacity="0.6"/>
            <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.8"/>
          </linearGradient>
          <filter id="glowGreen" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#10b981" flood-opacity="0.6"/>
          </filter>
          <filter id="glowBlue" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#3b82f6" flood-opacity="0.6"/>
          </filter>
          <filter id="glowRed" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#ef4444" flood-opacity="0.6"/>
          </filter>
          <filter id="glowYellow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#f59e0b" flood-opacity="0.6"/>
          </filter>
          <marker id="arrow" viewBox="0 0 10 10" refX="28" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#06b6d4" />
          </marker>
        </defs>
    `;

    // Render Edges (Prerequisite arrows)
    edges.forEach(edge => {
      const fromPos = nodePositions[edge.from];
      const toPos = nodePositions[edge.to];
      if (fromPos && toPos) {
        // Curve control point
        const midX = (fromPos.x + toPos.x) / 2;
        const midY = (fromPos.y + toPos.y) / 2 - 25;
        svgHtml += `
          <path d="M ${fromPos.x} ${fromPos.y} Q ${midX} ${midY} ${toPos.x} ${toPos.y}"
                fill="none" stroke="url(#edgeGrad)" stroke-width="2.5" stroke-dasharray="4 2" marker-end="url(#arrow)" />
        `;
      }
    });

    // Render Nodes
    nodes.forEach(node => {
      const pos = nodePositions[node.id];
      const color = node.color;
      let filter = "";
      if (node.status === "MASTERED") filter = 'filter="url(#glowGreen)"';
      else if (node.status === "LEARNING") filter = 'filter="url(#glowBlue)"';
      else if (node.status === "STRUGGLING") filter = 'filter="url(#glowRed)"';
      else if (node.status === "NEEDS_PRACTICE") filter = 'filter="url(#glowYellow)"';

      const iconSymbol = node.is_locked ? '🔒' : (node.status === 'MASTERED' ? '✓' : `${Math.round(node.mastery_score)}%`);

      svgHtml += `
        <g class="graph-node-group" onclick="KnowledgeGraphVisualizer.onNodeClick(${node.id})" 
           style="cursor: pointer;" transform="translate(${pos.x}, ${pos.y})">
          
          <!-- Outer Halo Ring -->
          <circle r="${nodeRadius + 4}" fill="none" stroke="${color}" stroke-width="1.5" stroke-opacity="0.4" />
          
          <!-- Main Node Circle -->
          <circle r="${nodeRadius}" fill="#0f172a" stroke="${color}" stroke-width="3" ${filter} />

          <!-- Center Text / Icon -->
          <text text-anchor="middle" dy="-2" fill="#fff" font-family="'Outfit', sans-serif" font-weight="700" font-size="13">
            ${iconSymbol}
          </text>
          
          <!-- Sequence Badge -->
          <circle cx="22" cy="-22" r="10" fill="${color}" />
          <text x="22" y="-18" text-anchor="middle" fill="#fff" font-size="9" font-weight="800">
            ${node.sequence_order}
          </text>

          <!-- Label below -->
          <text text-anchor="middle" y="${nodeRadius + 20}" fill="#e2e8f0" font-family="'Outfit', sans-serif" font-size="12" font-weight="600">
            ${node.code}
          </text>
          <text text-anchor="middle" y="${nodeRadius + 34}" fill="#94a3b8" font-family="'Plus Jakarta Sans', sans-serif" font-size="10">
            ${node.title.length > 20 ? node.title.substring(0, 18) + '...' : node.title}
          </text>
        </g>
      `;
    });

    svgHtml += `</svg>`;
    
    // Status legend
    const legendHtml = `
      <div style="display:flex; justify-content:center; gap:20px; flex-wrap:wrap; margin-top:16px;">
        <span class="badge badge-mastered"><span class="dot dot-green"></span> Mastered (≥70%)</span>
        <span class="badge badge-learning"><span class="dot dot-blue"></span> Learning (Active)</span>
        <span class="badge badge-practice"><span class="dot dot-yellow"></span> Needs Practice (40-69%)</span>
        <span class="badge badge-struggling"><span class="dot dot-red"></span> Struggling (&lt;40%)</span>
        <span class="badge badge-locked">🔒 Locked (Prerequisite Unmet)</span>
      </div>
    `;

    this.container.innerHTML = svgHtml + legendHtml;
  }

  static onNodeClick(conceptId) {
    if (window.handleConceptNodeClick) {
      window.handleConceptNodeClick(conceptId);
    } else {
      window.location.href = `/learning-gaps?concept_id=${conceptId}`;
    }
  }
}

window.KnowledgeGraphVisualizer = KnowledgeGraphVisualizer;
