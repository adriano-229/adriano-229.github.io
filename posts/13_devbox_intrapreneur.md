---
title: Business plan proposal
date: 2026-10-20
---

This plan follows the intrapreneur guidelines. Legal steps such as registration, licenses and insurance are not included
because the project would be developed inside
an existing company.

### DevBox

DevBox would be an internal tool for creating complete and identical development environments with one command. Each
environment would include the operating system, tools, dependencies and test services, and would run as a container on
the company's Kubernetes cluster.

New developers currently spend several days installing and configuring their computers. Teams also lose time solving "it
works on my machine" problems. DevBox would address both issues.

The first version would include a repository with versioned environment definitions and a small Python command-line tool
to create, start and delete environments. It would initially support one team's main project so that real users could
test it quickly.

The main alternatives are doing nothing, using shared setup documents, or using external services such as GitHub
Codespaces and Gitpod. DevBox would be different because it uses the company's own infrastructure, keeps code and data
in-house, and is adapted to the company's projects.

I would ask developers, the infrastructure team and HR for feedback. I would also check whether someone was already
working on a similar solution. The project would start with a short presentation to the directors and a pilot with one
volunteer team. The results would be measured by comparing onboarding time before and after the pilot.

I would lead the prototype as the intrapreneur. The infrastructure team would support the cluster, and a senior
developer would review the environment definitions.

### Financial projection

These are illustrative estimates:

- 20 developers, 8 new hires per year and an average cost of USD 20 per hour.
- Reducing onboarding from three days to half a day would save about 160 hours per year.
- Reducing environment-related problems by half would save about 500 hours per year.
- Total estimated savings: about USD 13,200 per year.
- First-year cost: about USD 5,800, including development and infrastructure.
- Estimated first-year benefit: about USD 7,400, with payback in five to six months.

In the short term, the goal would be to complete the pilot in three months. In twelve months, DevBox could support all
projects. In the long term, the same environments could be offered to clients and external collaborators.

The main risks are low adoption, maintenance costs and security problems in the shared cluster. These risks could be
reduced by involving developers and the infrastructure team from the beginning and by keeping the first version small.
