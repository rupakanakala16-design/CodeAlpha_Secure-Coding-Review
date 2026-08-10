document.addEventListener('DOMContentLoaded', () => {
    // 1. Animated Stat Counters
    const counters = document.querySelectorAll('[data-target]');
    counters.forEach(counter => {
        const target = Number(counter.dataset.target);
        const duration = 1400;
        const start = performance.now();

        function updateCounter(now) {
            const progress = Math.min((now - start) / duration, 1);
            // Ease out cubic
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            const value = Math.floor(easeProgress * target);
            counter.textContent = value;
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        }

        requestAnimationFrame(updateCounter);
    });

    // 2. Copy Code Buttons
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const codePanel = button.closest('.code-panel');
            const codeText = codePanel ? codePanel.querySelector('code')?.textContent || '' : '';
            if (!codeText) return;

            try {
                await navigator.clipboard.writeText(codeText);
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
                button.style.borderColor = 'rgba(74, 222, 128, 0.5)';
                button.style.color = '#4ade80';

                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.style.borderColor = '';
                    button.style.color = '';
                }, 1600);
            } catch (err) {
                console.error('Clipboard copy failed:', err);
            }
        });
    });

    // 3. Three.js 3D Cybersecurity Shield & Particle Network
    const canvasHost = document.getElementById('three-canvas');
    if (canvasHost && window.THREE) {
        const width = canvasHost.clientWidth || 500;
        const height = canvasHost.clientHeight || 440;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
        camera.position.z = 6.2;

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.setSize(width, height);
        canvasHost.appendChild(renderer.domElement);

        // Lighting
        const ambientLight = new THREE.AmbientLight(0x38bdf8, 1.8);
        scene.add(ambientLight);

        const pointLight1 = new THREE.PointLight(0x38bdf8, 3, 100);
        pointLight1.position.set(4, 3, 5);
        scene.add(pointLight1);

        const pointLight2 = new THREE.PointLight(0x4ade80, 2, 100);
        pointLight2.position.set(-4, -3, 3);
        scene.add(pointLight2);

        // Main Shield Group
        const shieldGroup = new THREE.Group();

        // Outer Wireframe Shield (Icosahedron)
        const shieldGeo = new THREE.IcosahedronGeometry(1.6, 2);
        const shieldMat = new THREE.MeshPhongMaterial({
            color: 0x38bdf8,
            emissive: 0x075985,
            wireframe: true,
            transparent: true,
            opacity: 0.35,
            shininess: 100
        });
        const shieldMesh = new THREE.Mesh(shieldGeo, shieldMat);
        shieldGroup.add(shieldMesh);

        // Inner Core Energy Sphere
        const coreGeo = new THREE.SphereGeometry(0.95, 32, 32);
        const coreMat = new THREE.MeshPhongMaterial({
            color: 0x60a5fa,
            emissive: 0x1d4ed8,
            transparent: true,
            opacity: 0.25,
            shininess: 80
        });
        const coreMesh = new THREE.Mesh(coreGeo, coreMat);
        shieldGroup.add(coreMesh);

        // Orbit Ring 1
        const ringGeo1 = new THREE.TorusGeometry(2.3, 0.03, 16, 120);
        const ringMat1 = new THREE.MeshBasicMaterial({
            color: 0x38bdf8,
            transparent: true,
            opacity: 0.65
        });
        const ring1 = new THREE.Mesh(ringGeo1, ringMat1);
        ring1.rotation.x = Math.PI / 3;
        ring1.rotation.y = Math.PI / 6;
        shieldGroup.add(ring1);

        // Orbit Ring 2 (Cross ring)
        const ringGeo2 = new THREE.TorusGeometry(2.6, 0.02, 16, 120);
        const ringMat2 = new THREE.MeshBasicMaterial({
            color: 0x4ade80,
            transparent: true,
            opacity: 0.45
        });
        const ring2 = new THREE.Mesh(ringGeo2, ringMat2);
        ring2.rotation.x = -Math.PI / 4;
        ring2.rotation.y = Math.PI / 4;
        shieldGroup.add(ring2);

        scene.add(shieldGroup);

        // Floating Cyber Particles Cloud
        const particleCount = 220;
        const particlePositions = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount * 3; i += 3) {
            particlePositions[i] = (Math.random() - 0.5) * 10;
            particlePositions[i + 1] = (Math.random() - 0.5) * 10;
            particlePositions[i + 2] = (Math.random() - 0.5) * 8;
        }

        const particlesGeo = new THREE.BufferGeometry();
        particlesGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

        const particlesMat = new THREE.PointsMaterial({
            color: 0x38bdf8,
            size: 0.04,
            transparent: true,
            opacity: 0.8
        });

        const particleSystem = new THREE.Points(particlesGeo, particlesMat);
        scene.add(particleSystem);

        // Network Node Lines
        const lineGroup = new THREE.Group();
        const lineCount = 18;
        for (let i = 0; i < lineCount; i++) {
            const p1 = new THREE.Vector3((Math.random() - 0.5) * 7, (Math.random() - 0.5) * 5, (Math.random() - 0.5) * 6);
            const p2 = new THREE.Vector3((Math.random() - 0.5) * 7, (Math.random() - 0.5) * 5, (Math.random() - 0.5) * 6);
            
            const lineGeo = new THREE.BufferGeometry().setFromPoints([p1, p2]);
            const lineMat = new THREE.LineBasicMaterial({
                color: 0x38bdf8,
                transparent: true,
                opacity: 0.22
            });
            const line = new THREE.Line(lineGeo, lineMat);
            lineGroup.add(line);
        }
        scene.add(lineGroup);

        // Animation Loop
        let clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);

            const elapsedTime = clock.getElapsedTime();

            // Rotate Shield
            shieldMesh.rotation.y = elapsedTime * 0.4;
            shieldMesh.rotation.x = Math.sin(elapsedTime * 0.5) * 0.2;

            coreMesh.rotation.y = -elapsedTime * 0.6;

            ring1.rotation.z = elapsedTime * 0.5;
            ring2.rotation.z = -elapsedTime * 0.4;

            particleSystem.rotation.y = elapsedTime * 0.15;
            particleSystem.rotation.x = Math.cos(elapsedTime * 0.2) * 0.1;

            lineGroup.rotation.y = elapsedTime * 0.2;

            renderer.render(scene, camera);
        }

        animate();

        // Responsive Resize Observer
        const resizeObserver = new ResizeObserver(() => {
            const w = canvasHost.clientWidth;
            const h = canvasHost.clientHeight;
            if (w && h) {
                camera.aspect = w / h;
                camera.updateProjectionMatrix();
                renderer.setSize(w, h);
            }
        });

        resizeObserver.observe(canvasHost);
    }
});
