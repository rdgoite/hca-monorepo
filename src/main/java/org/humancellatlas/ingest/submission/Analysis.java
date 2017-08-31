package org.humancellatlas.ingest.submission;

import lombok.Getter;
import org.humancellatlas.ingest.core.MetadataDocument;
import org.humancellatlas.ingest.core.Accession;
import org.humancellatlas.ingest.core.EntityType;
import org.humancellatlas.ingest.core.SubmissionDate;
import org.humancellatlas.ingest.core.UpdateDate;
import org.humancellatlas.ingest.core.Uuid;

/**
 * Javadocs go here!
 *
 * @author Tony Burdett
 * @date 30/08/17
 */
@Getter
public class Analysis extends MetadataDocument {
    protected Analysis(Uuid uuid,
                       SubmissionDate submissionDate,
                       UpdateDate updateDate,
                       Accession accession,
                       Object content) {
        super(EntityType.ANALYSIS, uuid, submissionDate, updateDate, accession, content);
    }
}
