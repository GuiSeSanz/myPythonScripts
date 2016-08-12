package rosalindExercices;

import java.util.ArrayList;
import java.util.List;

public class Access {
	public  String Id;
	public  String header;
	public  List<Integer> motifs;
	public String fasta;

	public Access(String Id) {
		this.Id = Id;
		this.motifs = new ArrayList<>();


	}
	public void setFasta(String fasta) {
		this.fasta = fasta;
	}
	public void setHeader(String header) {
		this.header = header;
	}
//	public void setMotifs(List<Integer> motifs) {
//		this.motifs = motifs;
//	}
	public void addToMotifs(int motifPosition) {
		this.motifs.add(motifPosition);
	}

	public String getId() {
		return Id;
	}

	public String getHeader() {
		return header;
	}

	public String getFasta() {
		return fasta;
	}

	public List<Integer> getMotifs() {
		return motifs;
	}
}