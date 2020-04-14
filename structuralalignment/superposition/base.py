"""
Base class for all the superposition engines.
"""
import logging

_logger = logging.getLogger(__name__)


class BaseAligner:
    def compute_sequence_alignment(self, algorithm, **kwargs):
        """
        Example implementation of first step
        """
        sequence_1 = self.structures[0].sequence()
        sequence_2 = self.structures[1].sequence()
        sequence_aligner = algorithm(**kwargs)
        alignment = sequence_aligner(sequence_1, sequence_2, **kwargs)
        return alignment

    def compute_structural_overlap(self, alignment, algorithm, **kwargs):
        structural_aligner = algorithm(**kwargs)
        rmsd_before = self.compute_rmsd(self.structures[0], self.structures[1])
        overlapped_1, overlapped_2 = structural_aligner(
            self.structures[0], self.structures[1], alignment
        )
        rmsd_after = self.compute_rmsd(overlapped_1, overlapped_2)
        _logger.log("RMSD before and after: %d, %d", rmsd_before, rmsd_after)
        return overlapped_1, overlapped_2, rmsd_after

    def calculate(self, structures, **kwargs):
        assert len(structures) == 2
        return self._calculate(structures, **kwargs)

    def _calculate(self, structures, *args, **kwargs):
        raise NotImplementedError("Reimplement in your subclass")
